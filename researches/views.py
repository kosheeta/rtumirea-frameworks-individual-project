from django.contrib import messages
from django.db.models import Avg, Count, Max, Min
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from homepage.views import not_found
from sources.models import Source
from users.models import User

from .forms import ResearchForm
from .models import Research

SORT_FIELDS = {
    "title": ("title",),
    "user": ("user__name", "title"),
    "count": ("-sources_count", "title"),
}


def researches_list(request):
    query = request.GET.get("q", "").strip()
    user_id = request.GET.get("user", "").strip()
    sort = request.GET.get("sort", "title")
    researches = Research.objects.select_related("user").annotate(
        sources_count=Count("sources")
    )
    if query:
        researches = researches.filter(title__icontains=query)
    if user_id.isdigit():
        researches = researches.filter(user_id=int(user_id))
    researches = researches.order_by(
        *SORT_FIELDS.get(sort, SORT_FIELDS["title"])
    )
    context = {
        "researches": researches,
        "users": User.objects.all(),
        "query": query,
        "selected_user": user_id,
        "sort": sort,
    }
    return render(request, "researches/research_list.html", context)


def research_detail(request, slug):
    try:
        research = Research.objects.select_related("user").get(slug=slug)
    except Research.DoesNotExist:
        return not_found(
            request, "Исследование не найдено",
            reverse("researches:list"), "к исследованиям",
        )
    sources = Source.objects.filter(research=research).not_excluded()
    sources = sources.select_related("user")
    stats = sources.aggregate(
        count=Count("id"),
        average_year=Avg("year"),
        oldest_year=Min("year"),
        newest_year=Max("year"),
    )
    relevances = [source.get_relevance() for source in sources]
    stats["actual_count"] = relevances.count("актуальный")
    stats["outdated_count"] = relevances.count("устаревший")
    context = {"research": research, "sources": sources, "stats": stats}
    return render(request, "researches/research_detail.html", context)


def research_create(request):
    form = ResearchForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        research = form.save()
        messages.success(request, "Исследование создано")
        return redirect(research.get_absolute_url())
    context = {"form": form, "title": "Новое исследование"}
    return render(request, "researches/research_form.html", context)


def research_edit(request, slug):
    research = get_object_or_404(Research, slug=slug)
    form = ResearchForm(
        request.POST or None, request.FILES or None, instance=research
    )
    if form.is_valid():
        research = form.save()
        messages.success(request, "Изменения сохранены")
        return redirect(research.get_absolute_url())
    context = {"form": form, "title": "Редактирование исследования",
               "research": research}
    return render(request, "researches/research_form.html", context)
