-- запросы сервиса учёта источников
-- проверка: sqlite3 data/sources.sqlite < sql/queries.sql

-- 1. список пользователей по алфавиту
SELECT id, name, email
FROM users
ORDER BY name;

-- 2. список источников, сначала новые
SELECT id, author, title, year
FROM sources
ORDER BY year DESC, title;

-- 3. источники не старше 2020 года (WHERE)
SELECT id, author, title, year
FROM sources
WHERE year >= 2020
ORDER BY year DESC;

-- 4. поиск источника по подстроке в авторе или названии (WHERE + LIKE)
SELECT id, author, title, year
FROM sources
WHERE title LIKE '%django%' OR author LIKE '%django%';

-- 5. исследования с именем владельца (JOIN)
SELECT researches.id, researches.title, users.name AS user_name
FROM researches
JOIN users ON researches.user_id = users.id
ORDER BY researches.title;

-- 6. источники с исследованием и пользователем, который их добавил (JOIN)
SELECT
    sources.id,
    sources.author,
    sources.title,
    sources.year,
    researches.title AS research_title,
    users.name AS user_name
FROM sources
JOIN researches ON sources.research_id = researches.id
JOIN users ON sources.user_id = users.id
ORDER BY sources.id;

-- 7. общее количество источников и средний год публикации (агрегаты)
SELECT COUNT(*) AS sources_count, ROUND(AVG(year), 1) AS average_year
FROM sources;

-- 8. самый старый и самый новый источник (агрегаты)
SELECT MIN(year) AS oldest_year, MAX(year) AS newest_year
FROM sources;

-- 9. количество источников и средний год по исследованиям (GROUP BY)
SELECT
    researches.id,
    researches.title,
    COUNT(sources.id) AS sources_count,
    ROUND(AVG(sources.year), 1) AS average_year
FROM researches
LEFT JOIN sources ON sources.research_id = researches.id
GROUP BY researches.id, researches.title
ORDER BY sources_count DESC;

-- 10. количество исследований и добавленных источников по пользователям (GROUP BY)
SELECT
    users.id,
    users.name,
    COUNT(DISTINCT researches.id) AS researches_count,
    COUNT(DISTINCT sources.id) AS sources_count
FROM users
LEFT JOIN researches ON researches.user_id = users.id
LEFT JOIN sources ON sources.user_id = users.id
GROUP BY users.id, users.name
ORDER BY users.name;

-- 11. распределение источников по актуальности (CASE + GROUP BY)
SELECT
    CASE
        WHEN CAST(strftime('%Y', 'now') AS INTEGER) - year <= 3
            THEN 'актуальный'
        WHEN CAST(strftime('%Y', 'now') AS INTEGER) - year <= 7
            THEN 'требует проверки'
        ELSE 'устаревший'
    END AS relevance,
    COUNT(*) AS sources_count
FROM sources
GROUP BY relevance
ORDER BY sources_count DESC;

-- 12. исследования, в которых не меньше 3 источников (HAVING)
SELECT researches.title, COUNT(sources.id) AS sources_count
FROM researches
JOIN sources ON sources.research_id = researches.id
GROUP BY researches.id, researches.title
HAVING COUNT(sources.id) >= 3;

-- 13. исследования со средним годом источников раньше 2020 (HAVING)
SELECT researches.title, ROUND(AVG(sources.year), 1) AS average_year
FROM researches
JOIN sources ON sources.research_id = researches.id
GROUP BY researches.id, researches.title
HAVING AVG(sources.year) < 2020;
