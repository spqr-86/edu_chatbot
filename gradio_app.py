import gradio as gr
from bot.chat_engine import ChatBot

# Инициализируем чат-бота
bot = ChatBot("data/courses.csv")

# Функция, принимающая сообщение от пользователя и возвращающая ответ бота
def chatbot_interface(message):
    response = bot.get_response(message)
    return response

# Создаем интерфейс Gradio
iface = gr.Interface(
    fn=chatbot_interface,
    inputs=gr.Textbox(lines=2, placeholder="Введите ваше сообщение..."),
    outputs=gr.Textbox(),
    title="EduFuture Chatbot",
    description="Введите сообщение и получите ответ от чат-бота."
)

if __name__ == "__main__":
    iface.launch()
