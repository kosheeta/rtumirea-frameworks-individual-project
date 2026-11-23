from django.shortcuts import render

from storage import load_all


def not_found(request, title, back_url, back_text):
    context = {"title": title, "back_url": back_url, "back_text": back_text}
    return render(request, "homepage/404.html", context, status=404)


def index(request):
    users, researches, sources = load_all()
    context = {
        "users_count": len(users),
        "researches_count": len(researches),
        "sources_count": len(sources),
    }
    return render(request, "homepage/index.html", context)


def page_not_found(request, exception):
    return render(request, "homepage/404.html", status=404)
