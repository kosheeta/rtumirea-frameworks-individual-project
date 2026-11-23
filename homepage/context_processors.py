from researches.models import Research
from sources.models import Source


def site_counts(request):
    # счётчики для меню на всех страницах
    return {
        "nav_researches_count": Research.objects.count(),
        "nav_sources_count": Source.objects.not_excluded().count(),
    }
