"""Тесты форм: фильтрация, создание, редактирование, исключение"""
import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from researches.models import Research
from sources.forms import SourceFilterForm, SourceForm
from sources.models import Source
from users.models import User

# минимальная картинка gif 1x1
GIF = (
    b"GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff!\xf9\x04"
    b"\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D"
    b"\x01\x00;"
)


@pytest.fixture
def data(db):
    user = User.objects.create(name="Иванова Анна", email="anna@example.com")
    research = Research.objects.create(user=user, title="Анализ данных")
    source = Source.objects.create(
        research=research, user=user, author="Иванов И. И.",
        title="Методы анализа", year=2022,
    )
    return {"user": user, "research": research, "source": source}


def source_data(data, **changes):
    values = {
        "research": data["research"].pk,
        "user": data["user"].pk,
        "author": "Петров П. П.",
        "title": "Новая книга",
        "year": 2023,
        "url": "https://example.org",
        "status": "new",
    }
    values.update(changes)
    return values


def test_filter_form_years(db):
    """Начальный год не может быть больше конечного"""
    form = SourceFilterForm({"year_from": 2024, "year_to": 2020})
    assert not form.is_valid()
    assert form.non_field_errors()
    assert not SourceFilterForm({"year_to": 3000}).is_valid()


def test_source_form_validation(data):
    """Проверка года, автора и дубликатов"""
    assert SourceForm(source_data(data)).is_valid()
    form = SourceForm(source_data(data, year=3000))
    assert "year" in form.errors
    form = SourceForm(source_data(data, author="123"))
    assert "author" in form.errors
    form = SourceForm(
        source_data(data, author="иванов и. и.", title="Методы анализа")
    )
    assert not form.is_valid()
    assert form.non_field_errors()


def test_edit_keeps_same_source_valid(data):
    """При редактировании источник не считается дубликатом самого себя"""
    form = SourceForm(
        source_data(data, author="Иванов И. И.", title="Методы анализа"),
        instance=data["source"],
    )
    assert form.is_valid()


def test_create_source_view(client, data):
    """Источник создаётся через POST и появляется в базе"""
    response = client.post(reverse("sources:create"), source_data(data))
    assert response.status_code == 302
    assert Source.objects.filter(title="Новая книга").exists()


def test_invalid_form_not_saved(client, data):
    """С ошибками форма показывается снова и ничего не сохраняет"""
    response = client.post(
        reverse("sources:create"), source_data(data, year="")
    )
    assert response.status_code == 200
    assert Source.objects.count() == 1


def test_edit_and_exclude(client, data):
    """Редактирование и исключение источника"""
    source = data["source"]
    client.post(
        reverse("sources:edit", args=[source.pk]),
        source_data(data, title="Изменённое название"),
    )
    source.refresh_from_db()
    assert source.title == "Изменённое название"
    assert client.get(
        reverse("sources:exclude", args=[source.pk])
    ).status_code == 405
    client.post(reverse("sources:exclude", args=[source.pk]))
    source.refresh_from_db()
    assert source.status == Source.Status.EXCLUDED


def test_delete_and_404(client, data):
    """Удаление через POST, несуществующий объект даёт 404"""
    source = data["source"]
    client.post(reverse("sources:delete", args=[source.pk]))
    assert not Source.objects.exists()
    assert client.get(
        reverse("sources:edit", args=[source.pk])
    ).status_code == 404


def test_research_with_cover(client, data, settings, tmp_path):
    """Исследование создаётся с картинкой"""
    settings.MEDIA_ROOT = tmp_path
    cover = SimpleUploadedFile("cover.gif", GIF, content_type="image/gif")
    response = client.post(reverse("researches:create"), {
        "user": data["user"].pk,
        "title": "Нейросети в медицине",
        "slug": "",
        "description": "Статья",
        "cover": cover,
    })
    assert response.status_code == 302
    research = Research.objects.get(title="Нейросети в медицине")
    assert research.slug == "neyroseti-v-meditsine"
    assert research.cover.name.startswith("researches/")
