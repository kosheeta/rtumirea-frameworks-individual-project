from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse

from homepage.views import not_found
from researches.models import Research
from users.models import User

from .models import Source

SORT_FIELDS = {
    "new": ("-year", "title"),
    "old": ("year", "title"),
    "author": ("author", "title"),
    "research": ("research__title", "-year"),
}


def sources_list(request):
    research_id = request.GET.get("research", "").strip()
    user_id = request.GET.get("user", "").strip()
    min_year = request.GET.get("year", "").strip()
    only_fresh = request.GET.get("fresh") == "1"
    status = request.GET.get("status", "").strip()
    sort = request.GET.get("sort", "new")
    error = None

    sources = Source.objects.with_related()
    if status in Source.Status.values:
        sources = sources.filter(status=status)
    if research_id.isdigit():
        sources = sources.filter(research_id=int(research_id))
    if user_id.isdigit():
        sources = sources.filter(user_id=int(user_id))
    if min_year:
        if min_year.isdigit():
            sources = sources.filter(year__gte=int(min_year))
        else:
            error = "Год должен быть числом"
    if only_fresh:
        # убираем устаревшие источники (старше 7 лет)
        sources = sources.fresh()
    sources = sources.order_by(*SORT_FIELDS.get(sort, SORT_FIELDS["new"]))

    page_obj = Paginator(sources, 5).get_page(request.GET.get("page"))
    params = request.GET.copy()
    params.pop("page", None)
    context = {
        "page_obj": page_obj,
        "sources": page_obj.object_list,
        "total": sources.count(),
        "researches": Research.objects.order_by("title"),
        "users": User.objects.order_by("name"),
        "selected_research": research_id,
        "selected_user": user_id,
        "min_year": min_year,
        "only_fresh": only_fresh,
        "sort": sort,
        "statuses": Source.Status.choices,
        "selected_status": status,
        "error": error,
        "query_string": params.urlencode(),
    }
    return render(request, "sources/source_list.html", context)


def sources_search(request):
    query = request.GET.get("q", "").strip()
    author_start = request.GET.get("author", "").strip()
    sources = Source.objects.none()
    searched = bool(query or author_start)
    if query:
        sources = Source.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        )
    if author_start:
        found = Source.objects.filter(author__istartswith=author_start)
        sources = sources & found if query else found
    sources = sources.with_related()
    context = {
        "sources": sources,
        "query": query,
        "author": author_start,
        "searched": searched,
    }
    return render(request, "sources/source_search.html", context)


def source_detail(request, source_id):
    source = (
        Source.objects.with_related()
        .filter(pk=source_id)
        .first()
    )
    if source is None:
        return not_found(
            request, "Источник не найден",
            reverse("sources:list"), "к источникам",
        )
    return render(request, "sources/source_detail.html", {"source": source})
