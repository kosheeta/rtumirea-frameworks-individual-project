"""Безопасный ввод данных"""


def input_int(prompt: str) -> int:
    """Запросить у пользователя целое число"""
    while True:
        raw_value = input(prompt)
        try:
            return int(raw_value)
        except ValueError:
            print("Ошибка: введите целое число")


def input_nonempty(prompt: str) -> str:
    """Запросить у пользователя непустую строку"""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Ошибка: значение не может быть пустым")
