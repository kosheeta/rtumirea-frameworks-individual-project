from django.shortcuts import render
from django.urls import reverse

from db.database import fetch_all, fetch_one
from homepage.views import not_found
from sources.views import SOURCE_FIELDS


def researches_list(request):
    researches = fetch_all("""
        SELECT
            researches.id,
            researches.title,
            researches.description,
            users.name AS user_name,
            COUNT(sources.id) AS sources_count
        FROM researches
        JOIN users ON researches.user_id = users.id
        LEFT JOIN sources ON sources.research_id = researches.id
        GROUP BY researches.id
        ORDER BY researches.title
    """)
    return render(
        request, "researches/research_list.html",
        {"researches": researches},
    )


def research_detail(request, research_id):
    research = fetch_one(
        """
        SELECT researches.*, users.name AS user_name
        FROM researches
        JOIN users ON researches.user_id = users.id
        WHERE researches.id = ?
        """,
        (research_id,),
    )
    if research is None:
        return not_found(
            request, "Исследование не найдено",
            reverse("researches:list"), "к исследованиям",
        )
    sources = fetch_all(
        f"SELECT {SOURCE_FIELDS} WHERE sources.research_id = ? "
        "ORDER BY sources.year DESC",
        (research_id,),
    )
    stats = {
        "count": len(sources),
        "average_year": fetch_one(
            "SELECT AVG(year) AS value FROM sources WHERE research_id = ?",
            (research_id,),
        )["value"],
        "actual_count": len(
            [s for s in sources if s["relevance"] == "актуальный"]
        ),
        "outdated_count": len(
            [s for s in sources if s["relevance"] == "устаревший"]
        ),
    }
    context = {"research": research, "sources": sources, "stats": stats}
    return render(request, "researches/research_detail.html", context)
