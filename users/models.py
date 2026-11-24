from typing import TYPE_CHECKING

from django.db import models

if TYPE_CHECKING:
    from django.db.models.manager import RelatedManager

    from researches.models import Research
    from sources.models import Source


class User(models.Model):
    name = models.CharField(max_length=200, verbose_name="Имя")
    email = models.EmailField(unique=True, verbose_name="Email")

    # обратные связи, нужны только для подсказок в ide
    if TYPE_CHECKING:
        researches: RelatedManager[Research]
        sources: RelatedManager[Source]

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
