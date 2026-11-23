from datetime import date

from django.db import models

from researches.models import Research
from users.models import User


class Source(models.Model):
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
    author = models.CharField(max_length=200, verbose_name="Автор")
    title = models.CharField(max_length=300, verbose_name="Название")
    year = models.PositiveIntegerField(verbose_name="Год публикации")
    url = models.URLField(blank=True, verbose_name="Ссылка")

    @staticmethod
    def fresh_border_year():
        return date.today().year - 7

    def get_age(self):
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

    def __str__(self):
        return f"{self.author} – {self.title}"

    class Meta:
        ordering = ["-year", "title"]
        verbose_name = "Источник"
        verbose_name_plural = "Источники"
