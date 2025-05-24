from aiogram import Dispatcher

from .garbage import GarbageMiddleware
from .throttling import ThrottlingMiddleware


def register(dispatcher: Dispatcher) -> None:
    middlewares = [
        GarbageMiddleware(),
        ThrottlingMiddleware(),
    ]

    for middleware in middlewares:
        dispatcher.update.middleware.register(middleware)
