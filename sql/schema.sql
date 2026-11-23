-- структура базы данных сервиса учёта источников

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS researches (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS sources (
    id INTEGER PRIMARY KEY,
    research_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    author TEXT NOT NULL,
    title TEXT NOT NULL,
    year INTEGER NOT NULL,
    url TEXT,
    FOREIGN KEY (research_id) REFERENCES researches(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
