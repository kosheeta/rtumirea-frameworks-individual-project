from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from homepage.views import not_found

from researches.models import Research

from .forms import SourceFilterForm, SourceForm
from .models import Source

SORT_FIELDS = {
    "new": ("-year", "title"),
    "old": ("year", "title"),
    "author": ("author", "title"),
    "research": ("research__title", "-year"),
}


def sources_list(request):
    form = SourceFilterForm(request.GET or None)
    sources = Source.objects.with_related()
    sort = "new"
    if form.is_valid():
        data = form.cleaned_data
        if data["research"]:
            sources = sources.filter(research=data["research"])
        if data["user"]:
            sources = sources.filter(user=data["user"])
        if data["status"]:
            sources = sources.filter(status=data["status"])
        if data["year_from"]:
            sources = sources.filter(year__gte=data["year_from"])
        if data["year_to"]:
            sources = sources.filter(year__lte=data["year_to"])
        if data["fresh"]:
            sources = sources.fresh()
        sort = data["sort"] or "new"
    elif form.is_bound:
        # при ошибках в форме показываем пустой список, а не всё подряд
        sources = sources.none()
    sources = sources.order_by(*SORT_FIELDS[sort])

    page_obj = Paginator(sources, 5).get_page(request.GET.get("page"))
    params = request.GET.copy()
    params.pop("page", None)
    context = {
        "form": form,
        "page_obj": page_obj,
        "sources": page_obj.object_list,
        "total": sources.count(),
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


def source_create(request):
    initial = {}
    research_slug = request.GET.get("research")
    if research_slug:
        research = Research.objects.filter(slug=research_slug).first()
        if research:
            initial = {"research": research, "user": research.user}
    form = SourceForm(request.POST or None, initial=initial)
    if form.is_valid():
        source = form.save()
        messages.success(request, f"Источник «{source.title}» добавлен")
        return redirect(source.get_absolute_url())
    context = {"form": form, "title": "Новый источник"}
    return render(request, "sources/source_form.html", context)


def source_edit(request, source_id):
    source = get_object_or_404(Source, pk=source_id)
    form = SourceForm(request.POST or None, instance=source)
    if form.is_valid():
        form.save()
        messages.success(request, "Изменения сохранены")
        return redirect(source.get_absolute_url())
    context = {"form": form, "title": "Редактирование источника",
               "source": source}
    return render(request, "sources/source_form.html", context)


@require_POST
def source_exclude(request, source_id):
    source = get_object_or_404(Source, pk=source_id)
    if source.status == Source.Status.EXCLUDED:
        source.status = Source.Status.NEW
        messages.info(request, "Источник возвращён в исследование")
    else:
        source.status = Source.Status.EXCLUDED
        messages.warning(request, "Источник исключён из исследования")
    source.save(update_fields=["status"])
    return redirect(source.get_absolute_url())


def source_delete(request, source_id):
    source = get_object_or_404(Source, pk=source_id)
    if request.method == "POST":
        research = source.research
        source.delete()
        messages.success(request, "Источник удалён")
        return redirect(research.get_absolute_url())
    return render(
        request, "sources/source_confirm_delete.html", {"source": source}
    )
