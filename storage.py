"""Сохранение и загрузка данных проекта в формате JSON"""
import json

from models import Research, Source, User
from models.researches import find_research
from models.users import find_user_by_id


def load_json(filename: str) -> list[dict]:
    """Загрузить список записей из JSON-файла"""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print(f"Ошибка: файл {filename} повреждён, данные не загружены")
        return []


def save_json(filename: str, data: list[dict]) -> None:
    """Сохранить список записей в JSON-файл"""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def load_users(filename: str) -> list[User]:
    """Загрузить пользователей из JSON-файла"""
    return [User.from_data(data) for data in load_json(filename)]


def save_users(filename: str, users: list[User]) -> None:
    """Сохранить пользователей в JSON-файл"""
    save_json(filename, [
        {"id": user.id, "name": user.name, "email": user.email}
        for user in users
    ])


def load_researches(filename: str, users: list[User]) -> list[Research]:
    """Загрузить исследования и связать их с пользователями"""
    researches = []
    for data in load_json(filename):
        user = find_user_by_id(users, data["user_id"])
        if user is None:
            print(f"Исследование #{data['id']} пропущено: нет пользователя")
            continue
        researches.append(
            Research(data["id"], user, data["title"], data["description"])
        )
    return researches


def save_researches(filename: str, researches: list[Research]) -> None:
    """Сохранить исследования в JSON-файл"""
    save_json(filename, [
        {
            "id": research.id,
            "user_id": research.user.id,
            "title": research.title,
            "description": research.description,
        }
        for research in researches
    ])


def load_sources(
    filename: str, researches: list[Research], users: list[User]
) -> list[Source]:
    """Загрузить источники и связать их с исследованиями и пользователями"""
    sources = []
    for data in load_json(filename):
        research = find_research(researches, data["research_id"])
        user = find_user_by_id(users, data["user_id"])
        if research is None or user is None:
            print(f"Источник #{data['id']} пропущен: нет связанных данных")
            continue
        sources.append(Source(
            data["id"], research, user, data["author"],
            data["title"], data["year"], data["url"],
        ))
    return sources


def save_sources(filename: str, sources: list[Source]) -> None:
    """Сохранить источники в JSON-файл"""
    save_json(filename, [
        {
            "id": source.id,
            "research_id": source.research.id,
            "user_id": source.user.id,
            "author": source.author,
            "title": source.title,
            "year": source.year,
            "url": source.url,
        }
        for source in sources
    ])
