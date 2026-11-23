from django.db import models
from django.urls import reverse

from users.models import User

from .utils import make_slug


class Research(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="researches",
        verbose_name="Владелец",
    )
    title = models.CharField(max_length=300, verbose_name="Название")
    slug = models.SlugField(
        max_length=60,
        unique=True,
        blank=True,
        verbose_name="Адрес (slug)",
        help_text="Латиницей, если не заполнить — создаётся из названия",
    )
    description = models.TextField(blank=True, verbose_name="Описание")
    cover = models.ImageField(
        upload_to="researches/",
        blank=True,
        verbose_name="Обложка",
        help_text="Картинка для страницы исследования, необязательно",
    )

    def belongs_to(self, user):
        return self.user_id == user.id

    def save(self, *args, **kwargs):
        if not self.slug:
            base = make_slug(self.title) or "research"
            slug = base
            number = 2
            while Research.objects.filter(slug=slug).exclude(
                pk=self.pk
            ).exists():
                slug = f"{base}-{number}"
                number += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("researches:detail", args=[self.slug])

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["title"]
        verbose_name = "Исследование"
        verbose_name_plural = "Исследования"
