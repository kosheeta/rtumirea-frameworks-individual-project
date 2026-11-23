"""Точка запуска приложения"""
from models import Research, Source, User
from models.researches import (
    add_research,
    find_research,
    get_user_researches,
)
from models.sources import (
    add_source,
    find_sources,
    get_research_sources,
    get_research_statistics,
    remove_source,
)
from models.users import add_user, find_user, find_user_by_id
from storage import (
    load_researches,
    load_sources,
    load_users,
    save_researches,
    save_sources,
    save_users,
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


def show_researches(researches: list[Research]) -> None:
    """Вывести список исследований"""
    if not researches:
        print("Исследования не найдены")
        return
    for research in researches:
        print(f"[{research.id}] {research}")


def show_users(users: list[User]) -> None:
    """Вывести список пользователей"""
    if not users:
        print("Пользователи не найдены")
        return
    for user in users:
        print(f"[{user.id}] {user}")


def show_sources(sources: list[Source]) -> None:
    """Вывести список источников с оценкой актуальности"""
    if not sources:
        print("Источники не найдены")
        return
    for source in sources:
        print(f"[{source.id}] {source} — {source.get_relevance()} "
              f"({source.get_age()} лет)")


def show_statistics(stats: dict) -> None:
    """Вывести статистику по источникам исследования"""
    if stats["count"] == 0:
        print("У исследования пока нет источников")
        return
    print(f"Источников: {stats['count']}")
    print(f"Средний год публикации: {stats['average_year']}")
    print(f"Актуальных источников: {stats['actual_count']}")
    print(f"Устаревших источников: {stats['outdated_count']}")


def ask_user(users: list[User]) -> User | None:
    """Запросить id пользователя и найти его"""
    user = find_user_by_id(users, input_int("Идентификатор пользователя: "))
    if user is None:
        print("Пользователь с таким идентификатором не найден")
    return user


def ask_research(researches: list[Research]) -> Research | None:
    """Запросить id исследования и найти его"""
    research = find_research(
        researches, input_int("Идентификатор исследования: ")
    )
    if research is None:
        print("Исследование с таким идентификатором не найдено")
    return research


def create_new_research(
    researches: list[Research], users: list[User]
) -> None:
    """Сценарий добавления исследования"""
    user = ask_user(users)
    if user is None:
        return
    title = input_nonempty("Название исследования: ")
    description = input_nonempty("Описание: ")
    research = add_research(researches, user, title, description)
    save_researches(RESEARCHES_FILE, researches)
    print(f"Добавлено исследование #{research.id}")


def create_new_source(
    sources: list[Source], researches: list[Research], users: list[User]
) -> None:
    """Сценарий добавления источника"""
    research = ask_research(researches)
    if research is None:
        return
    user = ask_user(users)
    if user is None:
        return
    author = input_nonempty("Автор: ")
    title = input_nonempty("Название источника: ")
    year = input_int("Год публикации: ")
    url = input_nonempty("Ссылка: ")
    if not Source.is_valid(author, title, year):
        print("Данные источника неполные")
        return
    source = add_source(sources, research, user, author, title, year, url)
    save_sources(SOURCES_FILE, sources)
    print(f"Добавлен источник #{source.id}")


def create_new_user(users: list[User]) -> None:
    """Сценарий добавления пользователя"""
    name = input_nonempty("Имя пользователя: ")
    email = input_nonempty("Email: ")
    if not User.is_email_valid(email):
        print("Некорректный email")
        return
    user = add_user(users, name, email)
    save_users(USERS_FILE, users)
    print(f"Добавлен пользователь #{user.id}")


def main() -> None:
    """Цикл меню приложения"""
    users = load_users(USERS_FILE)
    researches = load_researches(RESEARCHES_FILE, users)
    sources = load_sources(SOURCES_FILE, researches, users)

    while True:
        print(MENU)
        choice = input_nonempty("Выберите действие: ")

        match choice:
            case "1":
                show_researches(researches)
            case "2":
                research = ask_research(researches)
                if research:
                    show_sources(get_research_sources(sources, research))
            case "3":
                create_new_research(researches, users)
            case "4":
                create_new_source(sources, researches, users)
            case "5":
                query = input_nonempty("Строка поиска: ")
                show_sources(find_sources(sources, query))
            case "6":
                source_id = input_int("Идентификатор источника: ")
                if remove_source(sources, source_id):
                    save_sources(SOURCES_FILE, sources)
                    print("Источник удалён")
                else:
                    print("Источник не найден")
            case "7":
                research = ask_research(researches)
                if research:
                    show_statistics(
                        get_research_statistics(sources, research)
                    )
            case "8":
                show_users(users)
            case "9":
                create_new_user(users)
            case "10":
                query = input_nonempty("Строка поиска: ")
                show_users(find_user(users, query))
            case "11":
                user = ask_user(users)
                if user:
                    show_researches(get_user_researches(researches, user))
            case "0":
                print("Выход из программы")
                break
            case _:
                print("Неизвестный пункт меню")


if __name__ == "__main__":
    main()
