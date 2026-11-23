from django.contrib import admin

from sources.models import Source

from .models import Research


class SourceInline(admin.TabularInline):
    model = Source
    fields = ("author", "title", "year", "status", "user")
    extra = 0
    show_change_link = True
    autocomplete_fields = ("user",)


@admin.register(Research)
class ResearchAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "slug")
    list_select_related = ("user",)
    list_filter = ("user",)
    search_fields = ("title", "description", "user__name")
    ordering = ("title",)
    inlines = (SourceInline,)
    autocomplete_fields = ("user",)
