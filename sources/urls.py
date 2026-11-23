from django.urls import path

from . import views

app_name = "sources"

urlpatterns = [
    path("", views.sources_list, name="list"),
    path("search/", views.sources_search, name="search"),
    path("create/", views.source_create, name="create"),
    path("<int:source_id>/", views.source_detail, name="detail"),
    path("<int:source_id>/edit/", views.source_edit, name="edit"),
    path("<int:source_id>/exclude/", views.source_exclude, name="exclude"),
    path("<int:source_id>/delete/", views.source_delete, name="delete"),
]
