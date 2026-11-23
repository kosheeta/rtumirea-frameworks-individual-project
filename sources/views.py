from django.shortcuts import render
from django.urls import reverse

from db.database import AGE, RELEVANCE, fetch_all, fetch_one
from homepage.views import not_found

SOURCE_FIELDS = f"""
    sources.id,
    sources.author,
    sources.title,
    sources.year,
    sources.url,
    sources.research_id,
    sources.user_id,
    researches.title AS research_title,
    users.name AS user_name,
    {AGE} AS age,
    {RELEVANCE} AS relevance
FROM sources
JOIN researches ON sources.research_id = researches.id
JOIN users ON sources.user_id = users.id
"""


def sources_list(request):
    sources = fetch_all(
        f"SELECT {SOURCE_FIELDS} ORDER BY sources.year DESC, sources.title"
    )
    return render(request, "sources/source_list.html", {"sources": sources})


def sources_search(request):
    query = request.GET.get("q", "").strip()
    min_year = request.GET.get("year", "").strip()
    sources = []
    searched = bool(query or min_year)
    if searched:
        year = int(min_year) if min_year.isdigit() else 0
        sources = fetch_all(
            f"""
            SELECT {SOURCE_FIELDS}
            WHERE (py_lower(sources.title) LIKE ?
                OR py_lower(sources.author) LIKE ?)
            AND sources.year >= ?
            ORDER BY sources.year DESC
            """,
            (f"%{query.lower()}%", f"%{query.lower()}%", year),
        )
    context = {
        "sources": sources,
        "query": query,
        "min_year": min_year,
        "searched": searched,
    }
    return render(request, "sources/source_search.html", context)


def source_detail(request, source_id):
    source = fetch_one(
        f"SELECT {SOURCE_FIELDS} WHERE sources.id = ?", (source_id,)
    )
    if source is None:
        return not_found(
            request, "Источник не найден",
            reverse("sources:list"), "к источникам",
        )
    return render(request, "sources/source_detail.html", {"source": source})
