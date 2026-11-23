"""Класс источника и функции для работы с источниками"""
from __future__ import annotations

from datetime import date

from .researches import Research
from .users import User


class Source:
    """Источник литературы, использованный в исследовании"""

    def __init__(
        self,
        source_id: int,
        research: Research,
        user: User,
        author: str,
        title: str,
        year: int,
        url: str,
    ) -> None:
        self.id = source_id
        self.research = research
        self.user = user
        self.author = author
        self.title = title
        self.year = year
        self.url = url

    @staticmethod
    def is_valid(author: str, title: str, year: int) -> bool:
        """Проверить полноту данных источника"""
        return bool(author) and bool(title) and year > 0

    def get_age(self) -> int:
        """Вычислить возраст источника в годах на текущую дату"""
        return date.today().year - self.year

    def get_relevance(self) -> str:
        """Определить актуальность источника по его возрасту"""
        age = self.get_age()
        if age <= 3:
            return "актуальный"
        if age <= 7:
            return "требует проверки"
        return "устаревший"

    def format_citation(self) -> str:
        """Сформировать библиографическую запись источника"""
        return f"{self.author} {self.title} ({self.year}). {self.url}"

    def __str__(self) -> str:
        return self.format_citation()


def add_source(
    sources: list[Source],
    research: Research,
    user: User,
    author: str,
    title: str,
    year: int,
    url: str,
) -> Source:
    """Создать источник и добавить его в список sources"""
    # следующий свободный id, без переиспользования после удаления
    source_id = max((source.id for source in sources), default=0) + 1
    source = Source(source_id, research, user, author, title, year, url)
    sources.append(source)
    return source


def remove_source(sources: list[Source], source_id: int) -> bool:
    """Удалить источник по идентификатору"""
    for source in sources:
        if source.id == source_id:
            sources.remove(source)
            return True
    return False


def find_source(sources: list[Source], source_id: int) -> Source | None:
    """Найти источник по идентификатору"""
    for source in sources:
        if source.id == source_id:
            return source
    return None


def find_sources(sources: list[Source], query: str) -> list[Source]:
    """Найти источники по подстроке в названии или авторе"""
    query_lower = query.lower()
    return [
        source
        for source in sources
        if query_lower in source.title.lower()
        or query_lower in source.author.lower()
    ]


def filter_sources_by_year(
    sources: list[Source], min_year: int
) -> list[Source]:
    """Отобрать источники не раньше min_year"""
    return [source for source in sources if source.year >= min_year]


def sort_sources_by_year(sources: list[Source]) -> list[Source]:
    """Отсортировать источники по году публикации, от новых к старым"""
    return sorted(sources, key=lambda source: source.year, reverse=True)


def get_research_sources(
    sources: list[Source], research: Research
) -> list[Source]:
    """Отобрать источники, относящиеся к исследованию"""
    return [source for source in sources if source.research is research]


def get_research_statistics(
    sources: list[Source], research: Research
) -> dict:
    """Собрать статистику по источникам исследования"""
    research_sources = get_research_sources(sources, research)
    count = len(research_sources)
    if count == 0:
        return {
            "count": 0,
            "average_year": 0,
            "actual_count": 0,
            "outdated_count": 0,
        }

    total_years = sum(source.year for source in research_sources)
    relevances = [source.get_relevance() for source in research_sources]
    return {
        "count": count,
        "average_year": round(total_years / count, 1),
        "actual_count": relevances.count("актуальный"),
        "outdated_count": relevances.count("устаревший"),
    }
