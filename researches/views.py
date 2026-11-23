from django.http import HttpResponse

from homepage.views import not_found, page
from models.researches import find_research
from models.sources import get_research_sources, get_research_statistics
from sources.views import source_item
from storage import load_all


def researches_list(request):
    _, researches, _ = load_all()
    items = ""
    for research in researches:
        items += f"""
        <li class="list-group-item">
            <a href="/researches/{research.id}/">{research.title}</a>
            <div class="text-muted small">{research.user.name}</div>
        </li>
        """
    content = f"""
    <h1>Исследования</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Исследования", content))


def research_detail(request, research_id):
    _, researches, sources = load_all()
    research = find_research(researches, research_id)
    if research is None:
        return not_found(
            "Исследование не найдено", "/researches/", "к исследованиям"
        )
    research_sources = get_research_sources(sources, research)
    stats = get_research_statistics(sources, research)
    items = "".join(source_item(source) for source in research_sources)
    if not items:
        items = '<li class="list-group-item">Источников пока нет</li>'
    content = f"""
    <h1>{research.title}</h1>
    <p class="lead">{research.description}</p>
    <p>Автор: <a href="/users/{research.user.id}/">{research.user.name}</a></p>
    <div class="row mb-4">
        <div class="col">Источников: <b>{stats["count"]}</b></div>
        <div class="col">Средний год: <b>{stats["average_year"]}</b></div>
        <div class="col">Актуальных: <b>{stats["actual_count"]}</b></div>
        <div class="col">Устаревших: <b>{stats["outdated_count"]}</b></div>
    </div>
    <h4>Источники</h4>
    <ul class="list-group mb-3">{items}</ul>
    <a href="/researches/" class="btn btn-outline-secondary">
        ← к исследованиям</a>
    """
    return HttpResponse(page(research.title, content))
