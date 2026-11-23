from django.urls import path

from . import views

app_name = "researches"

urlpatterns = [
    path("", views.researches_list, name="list"),
    path("<slug:slug>/", views.research_detail, name="detail"),
]
