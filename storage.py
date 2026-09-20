"""Сохранение и загрузка данных проекта в формате JSON"""
import json


def load_json(filename: str) -> list[dict]:
    """Загрузить список записей из JSON-файла"""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print(f"Ошибка: файл {filename} повреждён, данные не загружены")
        return []


def save_json(filename: str, data: list[dict]) -> None:
    """Сохранить список записей в JSON-файл"""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
