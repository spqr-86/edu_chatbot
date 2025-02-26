import pandas as pd
import re
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import DataFrameLoader
from langchain.text_splitter import CharacterTextSplitter
from bot.config import OPENAI_API_KEY
from bot.faq_handler import FAQHandler

class ChatBot:
    def __init__(self, courses_csv: str):
        """Инициализирует чат-бота с памятью и загрузкой данных о курсах."""
        
        # Загружаем данные по курсам
        self.course_data = pd.read_csv(courses_csv)

        # Создаем векторное представление курсов
        self.vectorstore = self._create_course_vectorstore(self.course_data)

        # Инициализируем LLM с корректным API OpenAI
        self.llm = ChatOpenAI(
            openai_api_key=OPENAI_API_KEY,
            model_name="gpt-3.5-turbo",
            temperature=0.7
        )
        
        # Создаем память для хранения истории диалога
        self.memory = ConversationBufferMemory(
            memory_key="chat_history", 
            return_messages=True
        )
        
        # Инициализируем цепочку с поиском по курсам
        self.conversation = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vectorstore.as_retriever(),
            memory=self.memory
        )

        # Инициализируем обработчик FAQ
        self.faq_handler = FAQHandler()

    def _create_course_vectorstore(self, df: pd.DataFrame):
        """Создает векторный индекс для поиска информации по курсам."""
        df["text"] = df.apply(lambda row: f"Курс: {row['Название']}. Описание: {row['Описание']}. Цена: {row['Цена']} руб. Длительность: {row['Длительность']} часов.", axis=1)
        
        loader = DataFrameLoader(df, page_content_column="text")
        documents = loader.load()
        
        # Разбиваем на небольшие части (если курсы длинные)
        text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        texts = text_splitter.split_documents(documents)

        # Создаем векторное хранилище с FAISS
        vectorstore = FAISS.from_documents(
            texts, 
            OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
        )
        
        return vectorstore

    def get_courses_list(self) -> str:
        """Возвращает список всех доступных курсов (только названия)."""
        course_names = self.course_data['Название'].tolist()
        courses_text = "Вот список доступных курсов:\n"
        for i, name in enumerate(course_names, 1):
            courses_text += f"{i}. {name}\n"
        return courses_text

    def get_course_info(self, course_name, info_type='full'):
        """
        Возвращает информацию о конкретном курсе в зависимости от типа запроса.
        
        Параметры:
        - course_name: название курса или часть названия
        - info_type: тип информации ('full', 'description', 'price', 'duration')
        """
        # Ищем курс по части названия (регистронезависимый поиск)
        mask = self.course_data['Название'].str.lower().str.contains(course_name.lower())
        courses = self.course_data[mask]
        
        if courses.empty:
            return f"Извините, курс с названием '{course_name}' не найден."
        
        # Если найдено несколько курсов, используем первый
        if len(courses) > 1:
            result = f"Найдено несколько курсов с похожим названием. Информация о первом из них:\n\n"
            course = courses.iloc[0]
        else:
            result = ""
            course = courses.iloc[0]
        
        if info_type == 'full':
            result += (f"Курс: {course['Название']}\n"
                      f"Описание: {course['Описание']}\n"
                      f"Цена: {course['Цена']} руб.\n"
                      f"Длительность: {course['Длительность']} часов.")
        elif info_type == 'description':
            result += f"Описание курса '{course['Название']}': {course['Описание']}"
        elif info_type == 'price':
            result += f"Цена курса '{course['Название']}': {course['Цена']} руб."
        elif info_type == 'duration':
            result += f"Длительность курса '{course['Название']}': {course['Длительность']} часов."
        
        return result

    def handle_course_query(self, message):
        """Обрабатывает запросы, связанные с курсами."""
        message_lower = message.lower()
        
        # Проверяем запрос на список всех курсов
        if any(phrase in message_lower for phrase in [
            "список курсов", "какие курсы", "доступные курсы", "все курсы", 
            "перечисли курсы", "покажи курсы", "назови курсы"
        ]):
            return self.get_courses_list()
        
        # Проверяем запрос на информацию о конкретном курсе
        course_name_match = None
        info_type = 'full'
        
        # Поиск названия курса в запросе
        for name in self.course_data['Название']:
            if name.lower() in message_lower:
                course_name_match = name
                break
        
        # Если не нашли точное совпадение, попробуем найти часть названия (минимум 4 символа)
        if not course_name_match:
            words = re.findall(r'\b\w{4,}\b', message_lower)
            for word in words:
                mask = self.course_data['Название'].str.lower().str.contains(word)
                if mask.any():
                    course_name_match = word
                    break
        
        if course_name_match:
            # Определяем, какую информацию нужно предоставить
            if any(phrase in message_lower for phrase in ["описание", "о чем", "что такое", "подробнее"]):
                info_type = 'description'
            elif any(phrase in message_lower for phrase in ["цена", "стоимость", "сколько стоит"]):
                info_type = 'price'
            elif any(phrase in message_lower for phrase in ["длительность", "продолжительность", "как долго"]):
                info_type = 'duration'
            
            return self.get_course_info(course_name_match, info_type)
        
        # Если не смогли обработать запрос о курсах, возвращаем None
        return None

    def get_response(self, message: str) -> str:
        """Обрабатывает запрос пользователя: проверяет на FAQ, запросы о курсах и общие вопросы."""
        
        # Проверяем, есть ли ответ в FAQ
        faq_answer = self.faq_handler.find_answer(message)
        if faq_answer:
            return faq_answer
        
        # Проверяем, запрашивает ли пользователь информацию о курсах
        course_answer = self.handle_course_query(message)
        if course_answer:
            return course_answer
        
        # Если запрос не о курсах, используем LLM
        response = self.conversation({
            "question": message
        })
        
        return response["answer"]

if __name__ == "__main__":
    bot = ChatBot("data/courses.csv")  # Путь к CSV с курсами
    print("Добро пожаловать в EduFuture ChatBot! (Введите 'exit' или 'quit' для завершения.)")
    
    while True:
        user_input = input("Вы: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Бот: До свидания!")
            break
        response = bot.get_response(user_input)
        print(f"Бот: {response}")