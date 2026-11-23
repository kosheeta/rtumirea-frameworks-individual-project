from django.urls import path

from . import views

urlpatterns = [
    path("", views.researches_list, name="researches"),
    path("<int:research_id>/", views.research_detail, name="research_detail"),
]
