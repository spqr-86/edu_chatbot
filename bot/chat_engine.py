# bot/chat_engine.py
import openai
from bot.config import OPENAI_API_KEY
from bot.faq_handler import FAQHandler
from bot.memory import Memory
from bot.data_integration import CoursesData

class ChatBot:
    def __init__(self):
        self.client = openai.OpenAI(api_key=OPENAI_API_KEY)
        self.faq_handler = FAQHandler()
        self.memory = Memory()
        self.courses_data = CoursesData()

    def is_course_query(self, message):
        """
        Определяет, относится ли запрос к курсам, используя ключевые слова.
        """
        keywords = ["курс", "расписание", "инструктор", "программа", "обучение"]
        return any(keyword in message.lower() for keyword in keywords)

    def get_response(self, message):
        """
        Обрабатывает сообщение:
          1. Сначала ищет ответ в FAQ.
          2. Если запрос связан с курсами – ищет релевантную информацию из CSV.
          3. Иначе – добавляет сообщение в историю и обращается к OpenAI API.
        """
        # Проверка FAQ
        faq_answer = self.faq_handler.find_answer(message)
        if faq_answer:
            return faq_answer

        # Если запрос относится к курсам, ищем данные в CSV через LangChain
        if self.is_course_query(message):
            course_info = self.courses_data.query_courses(message)
            if course_info:
                return course_info

        # Добавляем сообщение пользователя в память
        self.memory.add_message("user", message)
        chat_history = self.memory.get_history()
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=chat_history
        )
        bot_response = response.choices[0].message.content.strip()
        self.memory.add_message("assistant", bot_response)
        return bot_response

if __name__ == "__main__":
    bot = ChatBot()
    while True:
        user_input = input("Вы: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Бот: До свидания!")
            break
        response = bot.get_response(user_input)
        print(f"Бот: {response}")
