from aiogram import Dispatcher

from . import main_menu, misc, profile


def bot_routers_include(dp: Dispatcher) -> None:
    dp.include_routers(
        *[
            main_menu.router,
            main_menu.dialog,
            profile.dialog,
            misc.router,
        ]
    )


__all__ = [
    "bot_routers_include",
]
