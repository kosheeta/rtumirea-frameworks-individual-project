from datetime import date

from django import forms

from researches.models import Research
from users.models import User

from .models import Source
from .validators import validate_author, validate_year

SORT_CHOICES = [
    ("new", "Сначала новые"),
    ("old", "Сначала старые"),
    ("author", "По автору"),
    ("research", "По исследованию"),
]


class SourceFilterForm(forms.Form):
    research = forms.ModelChoiceField(
        queryset=Research.objects.all(),
        required=False,
        empty_label="Все",
        label="Исследование",
    )
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        empty_label="Все",
        label="Добавил",
    )
    status = forms.ChoiceField(
        choices=[("", "Все"), *Source.Status.choices],
        required=False,
        label="Статус",
    )
    year_from = forms.IntegerField(required=False, label="С года")
    year_to = forms.IntegerField(required=False, label="По год")
    fresh = forms.BooleanField(required=False, label="Без устаревших")
    sort = forms.ChoiceField(
        choices=SORT_CHOICES, required=False, label="Сортировка"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == "fresh":
                field.widget.attrs["class"] = "form-check-input"
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs["class"] = "form-select"
            else:
                field.widget.attrs["class"] = "form-control"
        self.fields["year_from"].widget.attrs["placeholder"] = "2015"
        self.fields["year_to"].widget.attrs["placeholder"] = (
            str(date.today().year)
        )

    def clean_year_to(self):
        year_to = self.cleaned_data.get("year_to")
        if year_to and year_to > date.today().year:
            raise forms.ValidationError("Год не может быть в будущем")
        return year_to

    def clean(self):
        cleaned_data = super().clean()
        year_from = cleaned_data.get("year_from")
        year_to = cleaned_data.get("year_to")
        if year_from and year_to and year_from > year_to:
            raise forms.ValidationError(
                "Начальный год больше конечного"
            )
        return cleaned_data


class SourceForm(forms.ModelForm):
    author = forms.CharField(
        label="Автор",
        max_length=200,
        validators=[validate_author],
        help_text="Фамилия и инициалы, например: Иванов И. И.",
    )
    year = forms.IntegerField(
        label="Год публикации", validators=[validate_year]
    )

    class Meta:
        model = Source
        fields = ("research", "user", "author", "title", "year", "url",
                  "status")
        widgets = {
            "title": forms.TextInput(
                attrs={"placeholder": "Название книги или статьи"}
            ),
            "url": forms.URLInput(attrs={"placeholder": "https://"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs["class"] = "form-select"
            else:
                field.widget.attrs["class"] = "form-control"

    def clean_title(self):
        return " ".join(self.cleaned_data["title"].split())

    def clean(self):
        cleaned_data = super().clean()
        research = cleaned_data.get("research")
        author = cleaned_data.get("author")
        title = cleaned_data.get("title")
        if research and author and title:
            # один и тот же источник нельзя добавить в исследование дважды
            duplicates = Source.objects.filter(
                research=research,
                author__iexact=author,
                title__iexact=title,
            ).exclude(pk=self.instance.pk)
            if duplicates.exists():
                raise forms.ValidationError(
                    "Этот источник уже есть в выбранном исследовании"
                )
        return cleaned_data
