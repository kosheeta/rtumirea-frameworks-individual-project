"""Функции для работы с источниками"""
from datetime import date


def add_source(
    sources: list[dict],
    research_id: int,
    user_id: int,
    author: str,
    title: str,
    year: int,
    url: str,
) -> dict:
    """Добавить источник в список sources"""
    # следующий свободный id, без переиспользования после удаления
    source_id = max((source["id"] for source in sources), default=0) + 1
    source = {
        "id": source_id,
        "research_id": research_id,
        "user_id": user_id,
        "author": author,
        "title": title,
        "year": year,
        "url": url,
    }
    sources.append(source)
    return source


def remove_source(sources: list[dict], source_id: int) -> bool:
    """Удалить источник по идентификатору"""
    for source in sources:
        if source["id"] == source_id:
            sources.remove(source)
            return True
    return False


def find_sources(sources: list[dict], query: str) -> list[dict]:
    """Найти источники по подстроке в названии или авторе"""
    query_lower = query.lower()
    return [
        source
        for source in sources
        if query_lower in source["title"].lower()
        or query_lower in source["author"].lower()
    ]


def is_source_valid(author: str, title: str, year: int) -> bool:
    """Проверить полноту данных источника"""
    return bool(author) and bool(title) and year > 0


def filter_sources_by_year(sources: list[dict], min_year: int) -> list[dict]:
    """Отобрать источники не раньше min_year"""
    return [source for source in sources if source["year"] >= min_year]


def sort_sources_by_year(sources: list[dict]) -> list[dict]:
    """Отсортировать источники по году публикации, от новых к старым"""
    return sorted(sources, key=lambda source: source["year"], reverse=True)


def get_source_age(year: int) -> int:
    """Вычислить возраст источника в годах на текущую дату"""
    return date.today().year - year


def classify_source_relevance(age: int) -> str:
    """Определить актуальность источника по его возрасту"""
    if age <= 3:
        return "актуальный"
    if age <= 7:
        return "требует проверки"
    return "устаревший"


def format_citation(source: dict) -> str:
    """Сформировать библиографическую запись источника"""
    return (
        f"{source['author']} {source['title']} "
        f"({source['year']}). {source['url']}"
    )
