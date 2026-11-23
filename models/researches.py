"""Класс исследования и функции для работы с исследованиями"""
from __future__ import annotations

from .users import User


class Research:
    """Исследование, для которого собираются источники"""

    def __init__(
        self, research_id: int, user: User, title: str, description: str
    ) -> None:
        self.id = research_id
        self.user = user
        self.title = title
        self.description = description

    def belongs_to(self, user: User) -> bool:
        """Проверить, что исследование принадлежит пользователю"""
        return self.user.id == user.id

    def __str__(self) -> str:
        return f"{self.title}: {self.description} (автор: {self.user.name})"


def add_research(
    researches: list[Research], user: User, title: str, description: str
) -> Research:
    """Создать исследование и добавить его в список researches"""
    research_id = max(
        (research.id for research in researches), default=0
    ) + 1
    research = Research(research_id, user, title, description)
    researches.append(research)
    return research


def find_research(
    researches: list[Research], research_id: int
) -> Research | None:
    """Найти исследование по идентификатору"""
    for research in researches:
        if research.id == research_id:
            return research
    return None


def get_user_researches(
    researches: list[Research], user: User
) -> list[Research]:
    """Отобрать исследования пользователя"""
    return [research for research in researches if research.belongs_to(user)]
