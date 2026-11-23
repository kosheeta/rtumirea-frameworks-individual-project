from django.http import HttpResponse

BOOTSTRAP = (
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3"
    "/dist/css/bootstrap.min.css"
)


def page(title, content):
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <link rel="stylesheet" href="{BOOTSTRAP}">
</head>
<body>
    <nav class="navbar navbar-expand bg-body-tertiary mb-4">
        <div class="container">
            <a class="navbar-brand" href="/">Источники</a>
            <div class="navbar-nav">
                <a class="nav-link" href="/researches/">Исследования</a>
                <a class="nav-link" href="/sources/">Источники</a>
                <a class="nav-link" href="/users/">Пользователи</a>
            </div>
        </div>
    </nav>
    <main class="container">{content}</main>
</body>
</html>"""


def not_found(title, back_url, back_text):
    content = f"""
    <h1 class="text-danger">{title}</h1>
    <a href="{back_url}" class="btn btn-outline-secondary">← {back_text}</a>
    """
    return HttpResponse(page(title, content), status=404)


def index(request):
    content = """
    <h1 class="display-5">Сервис учёта использованных источников</h1>
    <p class="lead">
        Учёт источников литературы для научных и учебных исследований.
    </p>
    <a href="/researches/" class="btn btn-primary me-2">Исследования</a>
    <a href="/sources/" class="btn btn-secondary me-2">Источники</a>
    <a href="/users/" class="btn btn-outline-secondary">Пользователи</a>
    """
    return HttpResponse(page("Сервис учёта источников", content))


def page_not_found(request, exception):
    content = """
    <h1 class="text-danger">404 – страница не найдена</h1>
    <p>Проверьте адрес или вернитесь на главную.</p>
    <a href="/" class="btn btn-primary">На главную</a>
    """
    return HttpResponse(page("404 – страница не найдена", content),
                        status=404)
