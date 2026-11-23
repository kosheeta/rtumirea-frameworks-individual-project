"""Функции для работы с исследованиями"""
from __future__ import annotations

from sources import classify_source_relevance, get_source_age


def add_research(
    researches: list[dict], user_id: int, title: str, description: str
) -> dict:
    """Добавить исследование в список researches"""
    research_id = max(
        (research["id"] for research in researches), default=0
    ) + 1
    research = {
        "id": research_id,
        "user_id": user_id,
        "title": title,
        "description": description,
    }
    researches.append(research)
    return research


def find_research(researches: list[dict], research_id: int) -> dict | None:
    """Найти исследование по идентификатору"""
    for research in researches:
        if research["id"] == research_id:
            return research
    return None


def get_research_sources(
    sources: list[dict], research_id: int
) -> list[dict]:
    """Отобрать источники, относящиеся к исследованию"""
    return [
        source for source in sources if source["research_id"] == research_id
    ]


def get_research_statistics(sources: list[dict], research_id: int) -> dict:
    """Собрать статистику по источникам исследования"""
    research_sources = get_research_sources(sources, research_id)
    count = len(research_sources)
    if count == 0:
        return {
            "count": 0,
            "average_year": 0,
            "actual_count": 0,
            "outdated_count": 0,
        }

    total_years = sum(source["year"] for source in research_sources)
    actual_count = 0
    outdated_count = 0
    for source in research_sources:
        relevance = classify_source_relevance(get_source_age(source["year"]))
        if relevance == "актуальный":
            actual_count += 1
        elif relevance == "устаревший":
            outdated_count += 1

    return {
        "count": count,
        "average_year": round(total_years / count, 1),
        "actual_count": actual_count,
        "outdated_count": outdated_count,
    }
