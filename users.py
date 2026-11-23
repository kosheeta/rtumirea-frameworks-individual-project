"""Функции для работы с пользователями"""
from __future__ import annotations


def add_user(users: list[dict], name: str, email: str) -> dict:
    """Добавить пользователя в список users"""
    user_id = max((user["id"] for user in users), default=0) + 1
    user = {
        "id": user_id,
        "name": name,
        "email": email,
    }
    users.append(user)
    return user


def find_user(users: list[dict], user_id: int) -> dict | None:
    """Найти пользователя по идентификатору"""
    for user in users:
        if user["id"] == user_id:
            return user
    return None


def find_users(users: list[dict], query: str) -> list[dict]:
    """Найти пользователей по подстроке в имени или email"""
    query_lower = query.lower()
    return [
        user
        for user in users
        if query_lower in user["name"].lower()
        or query_lower in user["email"].lower()
    ]


def is_email_valid(email: str) -> bool:
    """Проверить корректность адреса электронной почты"""
    return "@" in email and "." in email.split("@")[-1]


def get_user_researches(
    researches: list[dict], user_id: int
) -> list[dict]:
    """Отобрать исследования пользователя"""
    return [
        research
        for research in researches
        if research["user_id"] == user_id
    ]
