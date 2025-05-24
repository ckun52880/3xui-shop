import logging
from typing import Any, Awaitable, Callable, MutableMapping

from aiogram import BaseMiddleware
from aiogram.dispatcher.flags import get_flag
from aiogram.types import Update
from cachetools import TTLCache

logger = logging.getLogger(__name__)


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(
        self,
        default_key: str | None = "default",
        default_ttl: float = 0.5,
        **ttl_map: dict[str, float],
    ) -> None:
        if default_key:
            ttl_map[default_key] = default_ttl

        self.default_key = default_key
        self.caches: dict[str, MutableMapping[int, None]] = {}

        for name, ttl in ttl_map.items():
            self.caches[name] = TTLCache(maxsize=10_000, ttl=ttl)

        logger.debug("Throttling Middleware initialized")

    async def __call__(
        self,
        handler: Callable[[Update, dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: dict[str, Any],
    ) -> Any:
        if event.pre_checkout_query or event.message and event.message.successful_payment:
            logger.debug("System event, skipping throttling")
            return await handler(event, data)

        user_id = event.event.from_user.id

        if not user_id:
            return await handler(event, data)

        key = get_flag(handler=data, name="throttling_key", default=self.default_key)
        cache = self.caches.get(key, self.caches["default"])

        if user_id in cache:
            logger.warning(f"User {user_id} throttled")
            return None

        cache[user_id] = None

        return await handler(event, data)
