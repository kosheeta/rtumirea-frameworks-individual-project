from django.shortcuts import render
from django.urls import reverse

from homepage.views import not_found
from models.sources import find_source
from storage import load_all


def sources_list(request):
    _, _, sources = load_all()
    return render(request, "sources/source_list.html", {"sources": sources})


def source_detail(request, source_id):
    _, _, sources = load_all()
    source = find_source(sources, source_id)
    if source is None:
        return not_found(
            request, "Источник не найден",
            reverse("sources:list"), "к источникам",
        )
    return render(request, "sources/source_detail.html", {"source": source})
