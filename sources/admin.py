from django.contrib import admin

from .models import Source


@admin.action(description="Отметить как проверенные")
def mark_checked(modeladmin, request, queryset):
    updated = queryset.update(status=Source.Status.CHECKED)
    modeladmin.message_user(request, f"Проверено источников: {updated}")


@admin.action(description="Исключить из исследования")
def mark_excluded(modeladmin, request, queryset):
    updated = queryset.update(status=Source.Status.EXCLUDED)
    modeladmin.message_user(request, f"Исключено источников: {updated}")


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = (
        "title", "author", "year", "status", "research", "user",
        "relevance",
    )
    list_display_links = ("title",)
    list_editable = ("year", "status")
    list_select_related = ("research", "user")
    list_filter = ("status", "research", "user", "year")
    search_fields = ("title", "author", "research__title")
    ordering = ("-year", "title")
    readonly_fields = ("short_name", "relevance")
    autocomplete_fields = ("research", "user")
    actions = (mark_checked, mark_excluded)
    list_per_page = 20
    fieldsets = (
        (None, {"fields": ("research", "user", "status")}),
        ("Описание источника", {"fields": ("author", "title", "year", "url")}),
        ("Вычисляемые поля", {"fields": ("short_name", "relevance")}),
    )

    @admin.display(description="Актуальность")
    def relevance(self, obj):
        return obj.get_relevance()
