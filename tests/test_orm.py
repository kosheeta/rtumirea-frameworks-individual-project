"""Тесты моделей Django и страниц на ORM"""
import pytest
from django.urls import reverse

from researches.models import Research
from sources.models import Source
from users.models import User


@pytest.fixture
def data(db):
    anna = User.objects.create(name="Иванова Анна", email="anna@example.com")
    ivan = User.objects.create(name="Петров Иван", email="ivan@example.com")
    research = Research.objects.create(user=anna, title="Анализ данных")
    Source.objects.create(
        research=research, user=anna, author="Иванов И. И.",
        title="Методы анализа", year=2022,
    )
    Source.objects.create(
        research=research, user=ivan, author="Смирнов А. А.",
        title="Машинное обучение", year=2010,
    )
    return {"anna": anna, "ivan": ivan, "research": research}


def test_relations(data):
    """Связи доступны в обе стороны через related_name"""
    research = data["research"]
    assert research.sources.count() == 2
    assert data["anna"].researches.first() == research
    assert data["ivan"].sources.first().research == research


def test_relevance_and_str(data):
    """Методы модели источника"""
    old = Source.objects.get(year=2010)
    assert old.get_relevance() == "устаревший"
    assert str(old) == "Смирнов А. А. – Машинное обучение"


def test_search_ignores_case(data):
    """Поиск по кириллице не зависит от регистра"""
    assert Source.objects.filter(title__icontains="МЕТОДЫ").count() == 1


def test_pages(client, data):
    """Основные страницы открываются, несуществующий объект даёт 404"""
    research_id = data["research"].id
    assert client.get(reverse("homepage:index")).status_code == 200
    assert client.get(reverse("homepage:statistics")).status_code == 200
    assert client.get(
        reverse("researches:detail", args=[research_id])
    ).status_code == 200
    assert client.get(
        reverse("researches:detail", args=[999])
    ).status_code == 404


def test_sources_filter_and_sort(client, data):
    """Фильтр по году и некорректный параметр не ломают страницу"""
    response = client.get(reverse("sources:list"), {"year": "2020"})
    assert response.context["total"] == 1
    response = client.get(reverse("sources:list"), {"year": "abc"})
    assert response.context["error"]
    response = client.get(reverse("sources:list"), {"sort": "bad"})
    assert response.status_code == 200
