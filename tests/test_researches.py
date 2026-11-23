"""Тесты класса Research и функций работы с исследованиями"""
from models import Research, User
from models.researches import (
    add_research,
    find_research,
    get_user_researches,
)


def test_research_creation():
    """Исследование хранит ссылку на объект пользователя"""
    user = User(1, "Иванова Анна", "ivanova@example.com")
    research = Research(1, user, "Анализ данных", "Курсовая работа")
    assert research.user is user
    assert research.belongs_to(user)
    assert "Иванова Анна" in str(research)


def test_add_and_find_research():
    """Исследования пользователя отбираются по владельцу"""
    anna = User(1, "Иванова Анна", "ivanova@example.com")
    ivan = User(2, "Петров Иван", "petrov@example.com")
    researches = []
    add_research(researches, anna, "Анализ данных", "Курсовая")
    add_research(researches, ivan, "Django", "Реферат")
    assert find_research(researches, 2).title == "Django"
    assert find_research(researches, 3) is None
    assert len(get_user_researches(researches, anna)) == 1
