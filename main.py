"""Точка запуска приложения"""
from researches import (
    add_research,
    find_research,
    get_research_sources,
    get_research_statistics,
)
from sources import (
    add_source,
    classify_source_relevance,
    find_sources,
    format_citation,
    get_source_age,
    remove_source,
)
from storage import load_json, save_json
from users import (
    add_user,
    find_user,
    find_users,
    get_user_researches,
    is_email_valid,
)
from utils import input_int, input_nonempty

RESEARCHES_FILE = "data/researches.json"
SOURCES_FILE = "data/sources.json"
USERS_FILE = "data/users.json"

MENU = """
=== Сервис учёта использованных источников ===

1. Показать исследования
2. Показать источники исследования
3. Добавить исследование
4. Добавить источник
5. Найти источники
6. Удалить источник
7. Показать статистику по исследованию
8. Показать пользователей
9. Добавить пользователя
10. Найти пользователей
11. Показать исследования пользователя
0. Выход
"""


def show_researches(researches: list[dict]) -> None:
    """Вывести список исследований"""
    if not researches:
        print("Исследования не найдены")
        return
    for research in researches:
        print(f"[{research['id']}] {research['title']}: "
              f"{research['description']}")


def show_users(users: list[dict]) -> None:
    """Вывести список пользователей"""
    if not users:
        print("Пользователи не найдены")
        return
    for user in users:
        print(f"[{user['id']}] {user['name']} <{user['email']}>")


def show_sources(sources: list[dict]) -> None:
    """Вывести список источников с оценкой актуальности"""
    if not sources:
        print("Источники не найдены")
        return
    for source in sources:
        age = get_source_age(source["year"])
        relevance = classify_source_relevance(age)
        citation = format_citation(source)
        print(f"[{source['id']}] {citation} — {relevance} ({age} лет)")


def show_statistics(stats: dict) -> None:
    """Вывести статистику по источникам исследования"""
    if stats["count"] == 0:
        print("У исследования пока нет источников")
        return
    print(f"Источников: {stats['count']}")
    print(f"Средний год публикации: {stats['average_year']}")
    print(f"Актуальных источников: {stats['actual_count']}")
    print(f"Устаревших источников: {stats['outdated_count']}")


def main() -> None:
    """Цикл меню приложения"""
    researches = load_json(RESEARCHES_FILE)
    sources = load_json(SOURCES_FILE)
    users = load_json(USERS_FILE)

    while True:
        print(MENU)
        choice = input_nonempty("Выберите действие: ")

        match choice:
            case "1":
                show_researches(researches)
            case "2":
                research_id = input_int("Идентификатор исследования: ")
                show_sources(get_research_sources(sources, research_id))
            case "3":
                user_id = input_int("Идентификатор пользователя: ")
                if find_user(users, user_id) is None:
                    print("Пользователь с таким идентификатором не найден")
                    continue
                title = input_nonempty("Название исследования: ")
                description = input_nonempty("Описание: ")
                research = add_research(
                    researches, user_id, title, description
                )
                save_json(RESEARCHES_FILE, researches)
                print(f"Добавлено исследование #{research['id']}")
            case "4":
                research_id = input_int("Идентификатор исследования: ")
                if find_research(researches, research_id) is None:
                    print("Исследование с таким идентификатором не найдено")
                    continue
                user_id = input_int("Идентификатор пользователя: ")
                if find_user(users, user_id) is None:
                    print("Пользователь с таким идентификатором не найден")
                    continue
                author = input_nonempty("Автор: ")
                title = input_nonempty("Название источника: ")
                year = input_int("Год публикации: ")
                url = input_nonempty("Ссылка: ")
                source = add_source(
                    sources, research_id, user_id, author, title, year, url
                )
                save_json(SOURCES_FILE, sources)
                print(f"Добавлен источник #{source['id']}")
            case "5":
                query = input_nonempty("Строка поиска: ")
                show_sources(find_sources(sources, query))
            case "6":
                source_id = input_int("Идентификатор источника: ")
                if remove_source(sources, source_id):
                    save_json(SOURCES_FILE, sources)
                    print("Источник удалён")
                else:
                    print("Источник не найден")
            case "7":
                research_id = input_int("Идентификатор исследования: ")
                show_statistics(get_research_statistics(sources, research_id))
            case "8":
                show_users(users)
            case "9":
                name = input_nonempty("Имя пользователя: ")
                email = input_nonempty("Email: ")
                if not is_email_valid(email):
                    print("Некорректный email")
                    continue
                user = add_user(users, name, email)
                save_json(USERS_FILE, users)
                print(f"Добавлен пользователь #{user['id']}")
            case "10":
                query = input_nonempty("Строка поиска: ")
                show_users(find_users(users, query))
            case "11":
                user_id = input_int("Идентификатор пользователя: ")
                show_researches(get_user_researches(researches, user_id))
            case "0":
                print("Выход из программы")
                break
            case _:
                print("Неизвестный пункт меню")


if __name__ == "__main__":
    main()
