import re

from django.db.backends.signals import connection_created


def like(pattern, value, escape="\\"):
    # like в sqlite не понимает регистр кириллицы, делаем свой
    if value is None or pattern is None:
        return False
    regex = ""
    i = 0
    while i < len(pattern):
        char = pattern[i]
        if char == escape and i + 1 < len(pattern):
            i += 1
            regex += re.escape(pattern[i])
        elif char == "%":
            regex += ".*"
        elif char == "_":
            regex += "."
        else:
            regex += re.escape(char)
        i += 1
    return re.fullmatch(regex, str(value), re.IGNORECASE | re.DOTALL)\
        is not None


def add_like(sender, connection, **kwargs):
    if connection.vendor == "sqlite":
        connection.connection.create_function("like", 2, like)
        connection.connection.create_function("like", 3, like)


connection_created.connect(add_like)
