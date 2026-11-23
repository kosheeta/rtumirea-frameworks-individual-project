"""Тесты класса Source и функций работы с источниками"""
from datetime import date

import pytest

from models import Research, Source, User
from models.sources import (
    add_source,
    find_sources,
    get_research_statistics,
    remove_source,
    sort_sources_by_year,
)


@pytest.fixture
def user():
    return User(1, "Иванова Анна", "ivanova@example.com")


@pytest.fixture
def research(user):
    return Research(1, user, "Анализ данных", "Курсовая работа")


def make_source(research, user, year=2022):
    return Source(
        1, research, user, "Иванов И. И.", "Методы анализа данных",
        year, "https://example.org"
    )


def test_source_creation(research, user):
    """Источник связан с исследованием и пользователем"""
    source = make_source(research, user)
    assert source.research is research
    assert source.user is user
    assert str(source) == (
        "Иванов И. И. Методы анализа данных (2022). https://example.org"
    )


def test_source_relevance(research, user):
    """Актуальность зависит от возраста источника в годах"""
    year = date.today().year
    assert make_source(research, user, year - 1).get_relevance() == (
        "актуальный"
    )
    assert make_source(research, user, year - 5).get_relevance() == (
        "требует проверки"
    )
    assert make_source(research, user, year - 10).get_relevance() == (
        "устаревший"
    )


def test_is_valid():
    """Источник без автора считается неполным"""
    assert Source.is_valid("Иванов И. И.", "Название", 2022) is True
    assert Source.is_valid("", "Название", 2022) is False


def test_add_find_remove_source(research, user):
    """Добавление, поиск и удаление источника"""
    sources = []
    add_source(
        sources, research, user, "Иванов И. И.", "Методы анализа данных",
        2022, "https://example.org"
    )
    assert sources[0].id == 1
    assert len(find_sources(sources, "анализа")) == 1
    assert len(find_sources(sources, "нет такого")) == 0
    assert remove_source(sources, 1) is True
    assert remove_source(sources, 1) is False


def test_sort_and_statistics(research, user):
    """Сортировка по году и статистика по исследованию"""
    sources = []
    add_source(sources, research, user, "А", "Первая", 2010, "url")
    add_source(sources, research, user, "Б", "Вторая", 2020, "url")
    assert sort_sources_by_year(sources)[0].year == 2020
    stats = get_research_statistics(sources, research)
    assert stats["count"] == 2
    assert stats["average_year"] == 2015
