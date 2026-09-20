"""Тесты функций сохранения и загрузки данных"""
from storage import load_json, save_json


def test_save_and_load_json(tmp_path):
    """Сохранённые данные читаются обратно без изменений"""
    filename = tmp_path / "data.json"
    data = [{"id": 1, "title": "Тест"}]
    save_json(str(filename), data)
    assert load_json(str(filename)) == data


def test_load_json_missing_file(tmp_path):
    """Отсутствие файла не приводит к ошибке"""
    filename = tmp_path / "missing.json"
    assert load_json(str(filename)) == []
