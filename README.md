# Edu ChatBot

## Описание
Чат-бот для образовательной платформы EduFuture, который использует:
- **LangChain** для ведения диалога с сохранением истории.
- **OpenAI API (GPT-3.5 Turbo)** для генерации ответов.
- **Локальную базу FAQ (CSV)** для быстрого ответа на типовые вопросы.

## Стек технологий
- Python
- LangChain
- OpenAI API
- Flask (планируется для веб-интерфейса)
- Docker (планируется для деплоя)
- pandas (для работы с CSV)
- pytest (для тестирования)

## Запуск
1. Клонируйте репозиторий.
2. Создайте виртуальное окружение и установите зависимости:
   ```bash
   python -m venv venv
   source venv/bin/activate  # для Mac/Linux
   venv\Scripts\activate     # для Windows
   pip install -r requirements.txt
