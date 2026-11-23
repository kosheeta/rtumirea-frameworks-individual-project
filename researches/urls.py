from django.urls import path

from . import views

app_name = "researches"

urlpatterns = [
    path("", views.researches_list, name="list"),
    path("create/", views.research_create, name="create"),
    path("<slug:slug>/", views.research_detail, name="detail"),
    path("<slug:slug>/edit/", views.research_edit, name="edit"),
]
