# bot/chat_engine.py
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from bot.config import OPENAI_API_KEY
from bot.faq_handler import FAQHandler

class ChatBot:
    def __init__(self):
        # Инициализируем LLM через LangChain
        self.llm = OpenAI(api_key=OPENAI_API_KEY, model_name="gpt-3.5-turbo")
        
        # Создаем модуль памяти для сохранения истории беседы
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        
        # Инициализируем цепочку для ведения диалога
        self.conversation = ConversationChain(llm=self.llm, memory=self.memory)
        
        # Инициализируем обработчик FAQ
        self.faq_handler = FAQHandler()

    def get_response(self, message: str) -> str:
        # Сначала проверяем, есть ли ответ в FAQ
        faq_answer = self.faq_handler.find_answer(message)
        if faq_answer:
            return faq_answer
        
        # Если нет, передаем запрос в цепочку диалога с сохранением контекста
        return self.conversation.run(message)

if __name__ == "__main__":
    bot = ChatBot()
    print("Добро пожаловать в EduFuture ChatBot! (Введите 'exit' или 'quit' для завершения.)")
    while True:
        user_input = input("Вы: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Бот: До свидания!")
            break
        response = bot.get_response(user_input)
        print(f"Бот: {response}")

