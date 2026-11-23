import re
from datetime import date

from django.core.exceptions import ValidationError


def validate_year(value):
    if value < 1450 or value > date.today().year:
        raise ValidationError(
            f"Год должен быть от 1450 до {date.today().year}"
        )


def validate_author(value):
    # фамилия и инициалы, например «Иванов И. И.»
    if not re.search(r"[A-Za-zА-Яа-яЁё]{2,}", value):
        raise ValidationError("Укажите фамилию автора")
    if re.search(r"\d", value):
        raise ValidationError("В имени автора не должно быть цифр")
