from django.http import HttpResponse

from homepage.views import not_found, page
from models.sources import find_source
from storage import load_all

BADGES = {
    "актуальный": "bg-success",
    "требует проверки": "bg-warning text-dark",
    "устаревший": "bg-secondary",
}


def source_item(source):
    relevance = source.get_relevance()
    return f"""
    <li class="list-group-item d-flex justify-content-between">
        <a href="/sources/{source.id}/">{source.author} – {source.title}</a>
        <span class="badge {BADGES[relevance]}">{relevance}</span>
    </li>
    """


def sources_list(request):
    _, _, sources = load_all()
    items = "".join(source_item(source) for source in sources)
    content = f"""
    <h1>Источники</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Источники", content))


def source_detail(request, source_id):
    _, _, sources = load_all()
    source = find_source(sources, source_id)
    if source is None:
        return not_found("Источник не найден", "/sources/", "к источникам")
    relevance = source.get_relevance()
    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">{source.title}</h5>
            <p class="card-text"><strong>Автор:</strong> {source.author}</p>
            <p class="card-text"><strong>Год:</strong> {source.year}
                ({source.get_age()} лет)</p>
            <p class="card-text"><strong>Ссылка:</strong>
                <a href="{source.url}">{source.url}</a></p>
            <p class="card-text"><strong>Исследование:</strong>
                <a href="/researches/{source.research.id}/">
                    {source.research.title}</a></p>
            <p class="card-text"><strong>Добавил:</strong>
                <a href="/users/{source.user.id}/">{source.user.name}</a></p>
            <p class="card-text">Актуальность:
                <span class="badge {BADGES[relevance]}">{relevance}</span></p>
            <p class="card-text"><strong>Библиографическая запись:</strong>
                {source.format_citation()}</p>
            <a href="/sources/" class="btn btn-outline-secondary">
                ← к источникам</a>
        </div>
    </div>
    """
    return HttpResponse(page(source.title, content))
