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
    assert client.get(reverse("homepage:index")).status_code == 200
    assert client.get(reverse("homepage:statistics")).status_code == 200
    assert client.get(
        data["research"].get_absolute_url()
    ).status_code == 200
    assert client.get(
        reverse("researches:detail", args=["net-takogo"])
    ).status_code == 404


def test_sources_filter_and_sort(client, data):
    """Фильтр по году и некорректный параметр не ломают страницу"""
    response = client.get(reverse("sources:list"), {"year_from": "2020"})
    assert response.context["total"] == 1
    response = client.get(reverse("sources:list"), {"year_from": "abc"})
    assert response.context["form"].errors
    response = client.get(reverse("sources:list"), {"sort": "bad"})
    assert response.status_code == 200


def test_slug_from_title(data):
    """Slug создаётся латиницей из названия и не повторяется"""
    assert data["research"].slug == "analiz-dannyh"
    second = Research.objects.create(user=data["ivan"], title="Анализ данных")
    assert second.slug == "analiz-dannyh-2"


def test_queryset_methods(data):
    """Методы менеджера и вычисляемое поле"""
    assert Source.objects.fresh().count() == 1
    assert Source.objects.outdated().count() == 1
    source = Source.objects.get(year=2022)
    assert source.short_name == "Иванов И. И., 2022"
    source.status = Source.Status.EXCLUDED
    source.save()
    assert Source.objects.not_excluded().count() == 1


def test_statistics_by_status(client, data):
    """Статистика учитывает статусы источников"""
    Source.objects.filter(year=2010).update(status=Source.Status.CHECKED)
    totals = client.get(reverse("homepage:statistics")).context["totals"]
    assert totals["checked_count"] == 1
    assert totals["new_count"] == 1


def test_admin_pages(admin_client, data):
    """Страницы админки открываются, поиск работает"""
    for name in ("users_user", "researches_research", "sources_source"):
        url = reverse(f"admin:{name}_changelist")
        assert admin_client.get(url).status_code == 200
    url = reverse("admin:sources_source_changelist")
    response = admin_client.get(url, {"q": "методы"})
    assert response.context["cl"].result_count == 1


def test_admin_action(admin_client, data):
    """Массовое действие меняет статус"""
    ids = list(Source.objects.values_list("id", flat=True))
    admin_client.post(
        reverse("admin:sources_source_changelist"),
        {"action": "mark_checked", "_selected_action": ids},
    )
    assert Source.objects.filter(status=Source.Status.CHECKED).count() == 2
