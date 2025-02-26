# tests/test_faq.py
import pytest
from bot.faq_handler import FAQHandler

@pytest.fixture
def faq():
    return FAQHandler()

def test_faq_answer_found(faq):
    assert faq.find_answer("Как войти в систему?") == "Перейдите на сайт и введите свои учетные данные."

def test_faq_answer_not_found(faq):
    assert faq.find_answer("Какой у вас адрес офиса?") is None
