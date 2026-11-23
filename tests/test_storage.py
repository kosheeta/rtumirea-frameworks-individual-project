"""Тесты функций сохранения и загрузки данных"""
from models import Research, Source, User
from storage import (
    load_json,
    load_researches,
    load_sources,
    load_users,
    save_json,
    save_researches,
    save_sources,
    save_users,
)


def test_save_and_load_json(tmp_path):
    """Сохранённые данные читаются обратно без изменений"""
    filename = tmp_path / "data.json"
    data = [{"id": 1, "title": "Тест"}]
    save_json(str(filename), data)
    assert load_json(str(filename)) == data


def test_load_json_missing_file(tmp_path):
    """Отсутствие файла не приводит к ошибке"""
    filename = tmp_path / "missing.json"
    assert load_json(str(filename)) == []


def test_save_and_load_objects(tmp_path):
    """После загрузки связи между объектами восстанавливаются"""
    user = User(1, "Иванова Анна", "ivanova@example.com")
    research = Research(1, user, "Анализ данных", "Курсовая")
    source = Source(1, research, user, "А", "Книга", 2020, "url")
    users_file = str(tmp_path / "users.json")
    researches_file = str(tmp_path / "researches.json")
    sources_file = str(tmp_path / "sources.json")
    save_users(users_file, [user])
    save_researches(researches_file, [research])
    save_sources(sources_file, [source])

    users = load_users(users_file)
    researches = load_researches(researches_file, users)
    sources = load_sources(sources_file, researches, users)
    assert sources[0].research is researches[0]
    assert researches[0].user is users[0]
    assert sources[0].title == "Книга"
