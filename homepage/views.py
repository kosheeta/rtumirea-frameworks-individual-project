from django.shortcuts import render

from db.database import RELEVANCE, fetch_all, fetch_one


def not_found(request, title, back_url, back_text):
    context = {"title": title, "back_url": back_url, "back_text": back_text}
    return render(request, "homepage/404.html", context, status=404)


def index(request):
    counts = fetch_one("""
        SELECT
            (SELECT COUNT(*) FROM users) AS users_count,
            (SELECT COUNT(*) FROM researches) AS researches_count,
            (SELECT COUNT(*) FROM sources) AS sources_count
    """)
    return render(request, "homepage/index.html", {"counts": counts})


def statistics(request):
    totals = fetch_one("""
        SELECT
            COUNT(*) AS sources_count,
            ROUND(AVG(year), 1) AS average_year,
            MIN(year) AS oldest_year,
            MAX(year) AS newest_year
        FROM sources
    """)
    by_research = fetch_all("""
        SELECT
            researches.id,
            researches.title,
            COUNT(sources.id) AS sources_count,
            ROUND(AVG(sources.year), 1) AS average_year
        FROM researches
        LEFT JOIN sources ON sources.research_id = researches.id
        GROUP BY researches.id
        ORDER BY sources_count DESC
    """)
    by_relevance = fetch_all(f"""
        SELECT {RELEVANCE} AS relevance, COUNT(*) AS sources_count
        FROM sources
        GROUP BY relevance
        ORDER BY sources_count DESC
    """)
    old_researches = fetch_all("""
        SELECT
            researches.id,
            researches.title,
            ROUND(AVG(sources.year), 1) AS average_year
        FROM researches
        JOIN sources ON sources.research_id = researches.id
        GROUP BY researches.id
        HAVING AVG(sources.year) < ?
    """, (2020,))
    context = {
        "totals": totals,
        "by_research": by_research,
        "by_relevance": by_relevance,
        "old_researches": old_researches,
    }
    return render(request, "homepage/statistics.html", context)


def page_not_found(request, exception):
    return render(request, "homepage/404.html", status=404)
