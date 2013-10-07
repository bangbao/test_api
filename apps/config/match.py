# coding: utf-8


def startswith(prefix):
    def decorator(value):
        return value.startswith(prefix)

    return decorator


def endswith(ends):
    def decorator(value):
        return value.endswith(ends)

    return decorator


def equalwith(name):
    def decorator(value):
        return name == value

    return decorator


def multiin(search):
    def decorator(value):
        return value in search

    return decorator


def rematch(pattern):
    import re

    return re.compile(pattern).match


def conform_with(func):
    def decorator(value):
        return func(value)

    return decorator

