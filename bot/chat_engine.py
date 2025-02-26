import openai
from bot.config import OPENAI_API_KEY
from bot.faq_handler import FAQHandler


class ChatBot:
    def __init__(self):
        self.client = openai.OpenAI(api_key=OPENAI_API_KEY)
        self.faq_handler = FAQHandler()

    def get_response(self, message):
        # Проверяем, есть ли ответ в FAQ
        faq_answer = self.faq_handler.find_answer(message)
        if faq_answer:
            return faq_answer
        
        # Если нет, идем в OpenAI API
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message}]
        )
        return response.choices[0].message.content.strip()

if __name__ == "__main__":
    bot = ChatBot()
    while True:
        user_input = input("Вы: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Бот: До свидания!")
            break
        response = bot.get_response(user_input)
        print(f"Бот: {response}")
