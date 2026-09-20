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
from utils import input_int, input_nonempty

RESEARCHES_FILE = "data/researches.json"
SOURCES_FILE = "data/sources.json"

MENU = """
=== Сервис учёта использованных источников ===

1. Показать исследования
2. Показать источники исследования
3. Добавить исследование
4. Добавить источник
5. Найти источники
6. Удалить источник
7. Показать статистику по исследованию
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

    while True:
        print(MENU)
        choice = input_nonempty("Выберите действие: ")

        if choice == "1":
            show_researches(researches)
        elif choice == "2":
            research_id = input_int("Идентификатор исследования: ")
            show_sources(get_research_sources(sources, research_id))
        elif choice == "3":
            title = input_nonempty("Название исследования: ")
            description = input_nonempty("Описание: ")
            research = add_research(researches, title, description)
            save_json(RESEARCHES_FILE, researches)
            print(f"Добавлено исследование #{research['id']}")
        elif choice == "4":
            research_id = input_int("Идентификатор исследования: ")
            if find_research(researches, research_id) is None:
                print("Исследование с таким идентификатором не найдено")
                continue
            author = input_nonempty("Автор: ")
            title = input_nonempty("Название источника: ")
            year = input_int("Год публикации: ")
            url = input_nonempty("Ссылка: ")
            source = add_source(
                sources, research_id, author, title, year, url
            )
            save_json(SOURCES_FILE, sources)
            print(f"Добавлен источник #{source['id']}")
        elif choice == "5":
            query = input_nonempty("Строка поиска: ")
            show_sources(find_sources(sources, query))
        elif choice == "6":
            source_id = input_int("Идентификатор источника: ")
            if remove_source(sources, source_id):
                save_json(SOURCES_FILE, sources)
                print("Источник удалён")
            else:
                print("Источник не найден")
        elif choice == "7":
            research_id = input_int("Идентификатор исследования: ")
            show_statistics(get_research_statistics(sources, research_id))
        elif choice == "0":
            print("Выход из программы")
            break
        else:
            print("Неизвестный пункт меню")


if __name__ == "__main__":
    main()
