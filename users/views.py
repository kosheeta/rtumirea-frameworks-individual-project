from django.db.models import Count
from django.shortcuts import render
from django.urls import reverse

from homepage.views import not_found

from .models import User


def users_list(request):
    users = User.objects.annotate(
        researches_count=Count("researches", distinct=True),
        sources_count=Count("sources", distinct=True),
    ).order_by("name")
    return render(request, "users/user_list.html", {"users": users})


def user_detail(request, user_id):
    user = User.objects.filter(pk=user_id).first()
    if user is None:
        return not_found(
            request, "Пользователь не найден",
            reverse("users:list"), "к пользователям",
        )
    context = {
        "user_obj": user,
        "researches": user.researches.order_by("title"),
        "sources_count": user.sources.count(),
    }
    return render(request, "users/user_detail.html", context)
