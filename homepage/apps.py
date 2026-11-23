from django.apps import AppConfig


class HomepageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'homepage'

    def ready(self):
        from . import sqlite_like  # noqa: F401
