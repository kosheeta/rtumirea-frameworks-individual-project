from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("researches/", include("researches.urls")),
    path("sources/", include("sources.urls")),
    path("users/", include("users.urls")),
]

if settings.DEBUG:
    urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))]

admin.site.site_header = "Сервис учёта источников"
admin.site.site_title = "Администрирование"
admin.site.index_title = "Управление данными"

handler404 = "homepage.views.page_not_found"
