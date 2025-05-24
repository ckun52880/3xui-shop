import logging
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import Update

from app.core.enums import Command

logger = logging.getLogger(__name__)


class GarbageMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        logger.debug("Garbage Middleware initialized")

    async def __call__(
        self,
        handler: Callable[[Update, dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: dict[str, Any],
    ) -> Any:
        user_id = event.event.from_user.id

        if (
            event.message
            and user_id != event.bot.id
            and event.message.text != f"/{Command.START.value.command}"
        ):
            await event.message.delete()
            logger.debug(f"Message ({event.message.content_type.value}) from {user_id} deleted")

        return await handler(event, data)
