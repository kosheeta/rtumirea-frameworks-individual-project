from django.shortcuts import render
from django.urls import reverse

from homepage.views import not_found
from models.researches import get_user_researches
from models.users import find_user_by_id
from storage import load_all


def users_list(request):
    users, _, _ = load_all()
    return render(request, "users/user_list.html", {"users": users})


def user_detail(request, user_id):
    users, researches, sources = load_all()
    user = find_user_by_id(users, user_id)
    if user is None:
        return not_found(
            request, "Пользователь не найден",
            reverse("users:list"), "к пользователям",
        )
    context = {
        "user_obj": user,
        "researches": get_user_researches(researches, user),
        "sources_count": len([s for s in sources if s.user is user]),
    }
    return render(request, "users/user_detail.html", context)
