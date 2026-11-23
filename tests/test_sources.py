"""Тесты функций работы с источниками"""
from sources import (
    add_source,
    classify_source_relevance,
    find_sources,
    is_source_valid,
    remove_source,
)


def test_add_source():
    """Добавленный источник появляется в списке с новым id"""
    sources = []
    add_source(
        sources, 1, 1, "Иванов И. И.", "Методы анализа данных",
        2022, "https://example.org"
    )
    assert len(sources) == 1
    assert sources[0]["id"] == 1


def test_find_sources():
    """Поиск находит источник по подстроке и не находит лишнего"""
    sources = []
    add_source(
        sources, 1, 1, "Иванов И. И.", "Методы анализа данных",
        2022, "https://example.org"
    )
    assert len(find_sources(sources, "анализа")) == 1
    assert len(find_sources(sources, "нет такого")) == 0


def test_remove_source():
    """Удаление по существующему id срабатывает один раз"""
    sources = []
    add_source(
        sources, 1, 1, "Иванов И. И.", "Методы анализа данных",
        2022, "https://example.org"
    )
    assert remove_source(sources, 1) is True
    assert len(sources) == 0
    assert remove_source(sources, 1) is False


def test_is_source_valid():
    """Источник без автора считается неполным"""
    assert is_source_valid("Иванов И. И.", "Название", 2022) is True
    assert is_source_valid("", "Название", 2022) is False


def test_classify_source_relevance():
    """Актуальность зависит от возраста источника в годах"""
    assert classify_source_relevance(1) == "актуальный"
    assert classify_source_relevance(5) == "требует проверки"
    assert classify_source_relevance(10) == "устаревший"
