"""Тесты класса User и функций работы с пользователями"""
from models import User
from models.users import add_user, find_user, find_user_by_id


def test_user_creation():
    """Атрибуты и строковое представление пользователя"""
    user = User(1, "Иванова Анна", "ivanova@example.com")
    assert user.id == 1
    assert user.name == "Иванова Анна"
    assert str(user) == "Иванова Анна <ivanova@example.com>"


def test_user_from_data():
    """Пользователь создаётся из данных JSON"""
    user = User.from_data(
        {"id": 2, "name": "Петров Иван", "email": "petrov@example.com"}
    )
    assert user.id == 2
    assert user.email == "petrov@example.com"


def test_add_and_find_user():
    """Добавленный пользователь находится по id и по email"""
    users = []
    add_user(users, "Иванова Анна", "ivanova@example.com")
    user = add_user(users, "Петров Иван", "petrov@example.com")
    assert user.id == 2
    assert find_user_by_id(users, 2) is user
    assert find_user_by_id(users, 5) is None
    assert len(find_user(users, "ivanova")) == 1


def test_is_email_valid():
    """Email без @ или домена считается некорректным"""
    assert User.is_email_valid("ivanova@example.com") is True
    assert User.is_email_valid("ivanova.example.com") is False
    assert User.is_email_valid("ivanova@example") is False
