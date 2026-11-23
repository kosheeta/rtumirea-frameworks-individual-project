from datetime import date

from django.db.models import Avg, Case, Count, F, Max, Min, Q, Value, When
from django.shortcuts import render

from researches.models import Research
from sources.models import Source
from users.models import User


def not_found(request, title, back_url, back_text):
    context = {"title": title, "back_url": back_url, "back_text": back_text}
    return render(request, "homepage/404.html", context, status=404)


def index(request):
    counts = {
        "users_count": User.objects.count(),
        "researches_count": Research.objects.count(),
        "sources_count": Source.objects.count(),
    }
    # только нужные поля, название исследования берём через F
    latest = (
        Source.objects.not_excluded()
        .annotate(research_title=F("research__title"))
        .values("id", "author", "title", "year", "research_title")[:3]
    )
    return render(
        request, "homepage/index.html", {"counts": counts, "latest": latest}
    )


def statistics(request):
    year = date.today().year
    totals = Source.objects.aggregate(
        sources_count=Count("id"),
        new_count=Count("id", filter=Q(status=Source.Status.NEW)),
        checked_count=Count("id", filter=Q(status=Source.Status.CHECKED)),
        excluded_count=Count("id", filter=Q(status=Source.Status.EXCLUDED)),
        average_year=Avg("year"),
        oldest_year=Min("year"),
        newest_year=Max("year"),
    )
    by_research = Research.objects.annotate(
        sources_count=Count(
            "sources",
            filter=~Q(sources__status=Source.Status.EXCLUDED),
        ),
        average_year=Avg("sources__year"),
    ).order_by("-sources_count", "title")
    by_relevance = (
        Source.objects.not_excluded().annotate(
            relevance=Case(
                When(year__gte=year - 3, then=Value("актуальный")),
                When(year__gte=year - 7, then=Value("требует проверки")),
                default=Value("устаревший"),
            )
        )
        .values("relevance")
        .annotate(sources_count=Count("id"))
        .order_by("-sources_count")
    )
    old_researches = (
        Research.objects.annotate(average_year=Avg("sources__year"))
        .filter(average_year__lt=2020)
        .order_by("average_year")
    )
    context = {
        "totals": totals,
        "by_research": by_research,
        "by_relevance": by_relevance,
        "old_researches": old_researches,
    }
    return render(request, "homepage/statistics.html", context)


def page_not_found(request, exception):
    return render(request, "homepage/404.html", status=404)
