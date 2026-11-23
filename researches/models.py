from django.db import models

from users.models import User


class Research(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="researches",
        verbose_name="Владелец",
    )
    title = models.CharField(max_length=300, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")

    def belongs_to(self, user):
        return self.user_id == user.id

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["title"]
        verbose_name = "Исследование"
        verbose_name_plural = "Исследования"
