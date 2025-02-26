import pytest
from bot.chat_engine import ChatBot
from bot.faq_handler import FAQHandler
from bot.data_integration import CoursesData


@pytest.fixture
def bot():
    return ChatBot()


def test_bot_response(bot):
    response = bot.get_response("Привет!")
    assert isinstance(response, str)


@pytest.fixture
def faq():
    return FAQHandler()

def test_faq_answer_found(faq):
    assert faq.find_answer("Как войти в систему?") == "Перейдите на сайт и введите свои учетные данные."

def test_faq_answer_not_found(faq):
    assert faq.find_answer("Какой у вас адрес офиса?") is None


def test_query_courses():
    courses = CoursesData(csv_path="data/courses.csv")
    # Простой тест: запрос, содержащий ключевое слово "Python"
    result = courses.query_courses("Расписание курса по Python")
    assert "Python" in result or "Python Programming" in result

