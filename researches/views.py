from django.shortcuts import render
from django.urls import reverse

from homepage.views import not_found
from models.researches import find_research
from models.sources import get_research_sources, get_research_statistics
from storage import load_all


def researches_list(request):
    _, researches, _ = load_all()
    return render(
        request, "researches/research_list.html",
        {"researches": researches},
    )


def research_detail(request, research_id):
    _, researches, sources = load_all()
    research = find_research(researches, research_id)
    if research is None:
        return not_found(
            request, "Исследование не найдено",
            reverse("researches:list"), "к исследованиям",
        )
    context = {
        "research": research,
        "sources": get_research_sources(sources, research),
        "stats": get_research_statistics(sources, research),
    }
    return render(request, "researches/research_detail.html", context)
