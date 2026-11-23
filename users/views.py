from django.shortcuts import render
from django.urls import reverse

from db.database import fetch_all, fetch_one
from homepage.views import not_found


def users_list(request):
    users = fetch_all("""
        SELECT
            users.id,
            users.name,
            users.email,
            COUNT(DISTINCT researches.id) AS researches_count,
            COUNT(DISTINCT sources.id) AS sources_count
        FROM users
        LEFT JOIN researches ON researches.user_id = users.id
        LEFT JOIN sources ON sources.user_id = users.id
        GROUP BY users.id
        ORDER BY users.name
    """)
    return render(request, "users/user_list.html", {"users": users})


def user_detail(request, user_id):
    user = fetch_one("SELECT * FROM users WHERE id = ?", (user_id,))
    if user is None:
        return not_found(
            request, "Пользователь не найден",
            reverse("users:list"), "к пользователям",
        )
    researches = fetch_all(
        "SELECT id, title FROM researches WHERE user_id = ? ORDER BY title",
        (user_id,),
    )
    sources_count = fetch_one(
        "SELECT COUNT(*) AS value FROM sources WHERE user_id = ?",
        (user_id,),
    )["value"]
    context = {
        "user_obj": user,
        "researches": researches,
        "sources_count": sources_count,
    }
    return render(request, "users/user_detail.html", context)
