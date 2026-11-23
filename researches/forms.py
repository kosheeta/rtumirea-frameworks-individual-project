from django import forms

from .models import Research


class ResearchForm(forms.ModelForm):
    class Meta:
        model = Research
        fields = ("user", "title", "slug", "description", "cover")
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs["class"] = "form-select"
            else:
                field.widget.attrs["class"] = "form-control"

    def clean_title(self):
        title = " ".join(self.cleaned_data["title"].split())
        if len(title) < 5:
            raise forms.ValidationError("Слишком короткое название")
        return title

    def clean_cover(self):
        cover = self.cleaned_data.get("cover")
        if cover and cover.size > 2 * 1024 * 1024:
            raise forms.ValidationError("Картинка должна быть меньше 2 МБ")
        return cover
