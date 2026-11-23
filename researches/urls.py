from django.urls import path

from . import views

app_name = "researches"

urlpatterns = [
    path("", views.researches_list, name="list"),
    path("<int:research_id>/", views.research_detail, name="detail"),
]
