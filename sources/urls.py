from django.urls import path

from . import views

app_name = "sources"

urlpatterns = [
    path("", views.sources_list, name="list"),
    path("search/", views.sources_search, name="search"),
    path("<int:source_id>/", views.source_detail, name="detail"),
]
