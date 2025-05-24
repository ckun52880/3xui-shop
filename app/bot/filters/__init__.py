from aiogram import Dispatcher

from .is_private import IsPrivate


def register(dispatcher: Dispatcher) -> None:
    dispatcher.update.filter(IsPrivate())
