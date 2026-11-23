from django.contrib import admin
from django.db.models import Count

from researches.models import Research

from .models import User


class ResearchInline(admin.TabularInline):
    model = Research
    fields = ("title", "slug")
    readonly_fields = ("slug",)
    extra = 0
    show_change_link = True


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "researches_count", "sources_count")
    search_fields = ("name", "email")
    ordering = ("name",)
    inlines = (ResearchInline,)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            researches_total=Count("researches", distinct=True),
            sources_total=Count("sources", distinct=True),
        )

    @admin.display(description="Исследований", ordering="researches_total")
    def researches_count(self, obj):
        return obj.researches_total

    @admin.display(description="Источников", ordering="sources_total")
    def sources_count(self, obj):
        return obj.sources_total
