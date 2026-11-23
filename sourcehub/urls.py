from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("researches/", include("researches.urls")),
    path("sources/", include("sources.urls")),
    path("users/", include("users.urls")),
]

handler404 = "homepage.views.page_not_found"
