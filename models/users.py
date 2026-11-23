"""Класс пользователя и функции для работы с пользователями"""
from __future__ import annotations


class User:
    """Пользователь сервиса"""

    def __init__(self, user_id: int, name: str, email: str) -> None:
        self.id = user_id
        self.name = name
        self.email = email

    @classmethod
    def from_data(cls, data: dict) -> User:
        """Создать пользователя из данных JSON"""
        return cls(data["id"], data["name"], data["email"])

    @staticmethod
    def is_email_valid(email: str) -> bool:
        """Проверить корректность адреса электронной почты"""
        return "@" in email and "." in email.split("@")[-1]

    def __str__(self) -> str:
        return f"{self.name} <{self.email}>"


def add_user(users: list[User], name: str, email: str) -> User:
    """Создать пользователя и добавить его в список users"""
    user_id = max((user.id for user in users), default=0) + 1
    user = User(user_id, name, email)
    users.append(user)
    return user


def find_user_by_id(users: list[User], user_id: int) -> User | None:
    """Найти пользователя по идентификатору"""
    for user in users:
        if user.id == user_id:
            return user
    return None


def find_user(users: list[User], query: str) -> list[User]:
    """Найти пользователей по подстроке в имени или email"""
    query_lower = query.lower()
    return [
        user
        for user in users
        if query_lower in user.name.lower()
        or query_lower in user.email.lower()
    ]
