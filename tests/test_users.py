"""Тесты функций работы с пользователями"""
from users import add_user, find_user, find_users, is_email_valid


def test_add_user():
    """Добавленный пользователь получает следующий id"""
    users = []
    add_user(users, "Иванова Анна", "ivanova@example.com")
    add_user(users, "Петров Иван", "petrov@example.com")
    assert len(users) == 2
    assert users[1]["id"] == 2


def test_find_user():
    """Пользователь находится по id и по подстроке email"""
    users = []
    add_user(users, "Иванова Анна", "ivanova@example.com")
    assert find_user(users, 1)["name"] == "Иванова Анна"
    assert find_user(users, 5) is None
    assert len(find_users(users, "ivanova")) == 1


def test_is_email_valid():
    """Email без @ или домена считается некорректным"""
    assert is_email_valid("ivanova@example.com") is True
    assert is_email_valid("ivanova.example.com") is False
    assert is_email_valid("ivanova@example") is False
