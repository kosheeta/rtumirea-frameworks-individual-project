from django.db import migrations, models

from researches.utils import make_slug


def fill_slugs(apps, schema_editor):
    Research = apps.get_model("researches", "Research")
    used = set()
    for research in Research.objects.all():
        slug = make_slug(research.title) or "research"
        if slug in used:
            slug = f"{slug}-{research.pk}"
        used.add(slug)
        research.slug = slug
        research.save(update_fields=["slug"])


class Migration(migrations.Migration):

    dependencies = [
        ("researches", "0001_initial"),
    ]

    operations = [
        # сначала поле без unique, заполняем, потом делаем уникальным
        migrations.AddField(
            model_name="research",
            name="slug",
            field=models.SlugField(
                blank=True, max_length=60, verbose_name="Адрес (slug)"
            ),
        ),
        migrations.RunPython(fill_slugs, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="research",
            name="slug",
            field=models.SlugField(
                blank=True,
                help_text="Латиницей, если не заполнить — "
                          "создаётся из названия",
                max_length=60,
                unique=True,
                verbose_name="Адрес (slug)",
            ),
        ),
    ]
