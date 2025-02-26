import gradio as gr
from bot.chat_engine import ChatBot

# Инициализируем чат-бота
bot = ChatBot()

# Функция, которая будет вызвана при вводе сообщения в интерфейсе
def chatbot_interface(message):
    response = bot.get_response(message)
    return response

# Создаем интерфейс Gradio:
# - inputs: текстовое поле для ввода сообщения
# - outputs: текстовое поле для вывода ответа
iface = gr.Interface(
    fn=chatbot_interface,
    inputs=gr.inputs.Textbox(lines=2, placeholder="Введите ваше сообщение..."),
    outputs="text",
    title="EduFuture Chatbot",
    description="Введите сообщение и получите ответ от чат-бота."
)

if __name__ == "__main__":
    # Запуск локального веб-сервера, а также создание публичной ссылки (при желании)
    iface.launch()