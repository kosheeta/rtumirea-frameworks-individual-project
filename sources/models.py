from datetime import date
from typing import ClassVar

from django.db import models
from django.db.models import F, Value
from django.db.models.functions import Concat
from django.urls import reverse

from researches.models import Research
from users.models import User


def fresh_border_year():
    return date.today().year - 7


class SourceQuerySet(models.QuerySet["Source"]):
    def with_related(self):
        return self.select_related("research", "user")

    def not_excluded(self):
        return self.exclude(status=Source.Status.EXCLUDED)

    def fresh(self):
        return self.filter(year__gte=fresh_border_year())

    def outdated(self):
        return self.filter(year__lt=fresh_border_year())

    def with_age(self):
        return self.annotate(age=Value(date.today().year) - F("year"))


class Source(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "Новый"
        CHECKED = "checked", "Проверен"
        EXCLUDED = "excluded", "Исключён"

    research = models.ForeignKey(
        Research,
        on_delete=models.CASCADE,
        related_name="sources",
        verbose_name="Исследование",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="sources",
        verbose_name="Добавил",
    )
    author = models.CharField(
        max_length=200,
        verbose_name="Автор",
        help_text="Например: Иванов И. И.",
    )
    title = models.CharField(max_length=300, verbose_name="Название")
    year = models.PositiveIntegerField(verbose_name="Год публикации")
    url = models.URLField(blank=True, verbose_name="Ссылка")
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.NEW,
        verbose_name="Статус",
    )
    short_name = models.GeneratedField(
        expression=Concat("author", Value(", "), "year"),
        output_field=models.CharField(max_length=220),
        db_persist=True,
        verbose_name="Краткая ссылка",
    )

    # as_manager() даёт менеджер с методами SourceQuerySet,
    # аннотация нужна чтобы ide видела with_related(), fresh() и т.д.
    objects: ClassVar[SourceQuerySet] = (  # pyright: ignore
        SourceQuerySet.as_manager()  # pyright: ignore
    )

    @staticmethod
    def fresh_border_year():
        return fresh_border_year()

    def get_age(self) -> int:
        return date.today().year - self.year

    def get_relevance(self):
        age = self.get_age()
        if age <= 3:
            return "актуальный"
        if age <= 7:
            return "требует проверки"
        return "устаревший"

    def format_citation(self):
        return f"{self.author} {self.title} ({self.year}). {self.url}"

    def get_absolute_url(self):
        return reverse("sources:detail", args=[self.pk])

    def __str__(self) -> str:
        return f"{self.author} – {self.title}"

    class Meta:
        ordering = ["-year", "title"]
        verbose_name = "Источник"
        verbose_name_plural = "Источники"
