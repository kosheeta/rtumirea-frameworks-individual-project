from django.http import HttpResponse

from homepage.views import not_found, page
from models.researches import get_user_researches
from models.users import find_user_by_id
from storage import load_all


def users_list(request):
    users, _, _ = load_all()
    items = ""
    for user in users:
        items += f"""
        <li class="list-group-item d-flex justify-content-between">
            <a href="/users/{user.id}/">{user.name}</a>
            <span class="text-muted">{user.email}</span>
        </li>
        """
    content = f"""
    <h1>Пользователи</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Пользователи", content))


def user_detail(request, user_id):
    users, researches, sources = load_all()
    user = find_user_by_id(users, user_id)
    if user is None:
        return not_found(
            "Пользователь не найден", "/users/", "к пользователям"
        )
    items = ""
    for research in get_user_researches(researches, user):
        items += f"""
        <li class="list-group-item">
            <a href="/researches/{research.id}/">{research.title}</a>
        </li>
        """
    if not items:
        items = '<li class="list-group-item">Исследований пока нет</li>'
    added = len([source for source in sources if source.user is user])
    content = f"""
    <h1>{user.name}</h1>
    <p>Email: {user.email}</p>
    <p>Добавлено источников: {added}</p>
    <h4>Исследования</h4>
    <ul class="list-group mb-3">{items}</ul>
    <a href="/users/" class="btn btn-outline-secondary">
        ← к пользователям</a>
    """
    return HttpResponse(page(user.name, content))
