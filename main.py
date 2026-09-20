from datetime import date

source_author = "Иванов И. И."
source_title = "Методы анализа данных"
source_year_raw = "2022"
source_url = "https://example.org/articles/data-analysis"


def is_source_valid(author, title, year):
    return bool(author) and bool(title) and year > 0


def format_citation(author, title, year, url):
    return f"{author} {title} ({year}). {url}"


def get_source_age(year):
    current_year = date.today().year
    return current_year - year


def classify_source_relevance(age):
    if age <= 3:
        return "актуальный"
    elif age <= 7:
        return "требует проверки"
    else:
        return "устаревший"


source_year = int(source_year_raw)

print(f"Источник: {source_title}")
print(f"Автор: {source_author}")
print(f"Год публикации: {source_year}")

if is_source_valid(source_author, source_title, source_year):
    citation = format_citation(source_author, source_title, source_year, source_url)
    age = get_source_age(source_year)
    relevance = classify_source_relevance(age)

    print(f"Библиографическая запись: {citation}")
    print(f"Возраст источника: {age} лет")
    print(f"Актуальность: {relevance}")
else:
    print("Источник содержит неполные данные и не может быть добавлен")
