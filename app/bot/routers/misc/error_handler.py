import logging
import traceback

from aiogram import Router
from aiogram.exceptions import (
    TelegramBadRequest,
    TelegramForbiddenError,
    TelegramNotFound,
)
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import BufferedInputFile, ErrorEvent
from aiogram.utils.formatting import Bold, Code, Text

from app.core.config import Config

logger = logging.getLogger(__name__)
router = Router(name=__name__)


@router.errors(ExceptionTypeFilter(Exception))
async def errors_handler(event: ErrorEvent) -> bool:
    if isinstance(event.exception, TelegramForbiddenError):
        logger.info(f"User {event.update.message.from_user.id} blocked the bot")
        return True

    if isinstance(event.exception, TelegramBadRequest):
        logger.warning(
            f"User {event.update.callback_query.from_user.id} bad request for edit/send message"
        )
        return True

    if isinstance(event.exception, TelegramNotFound):
        logger.info(f"User {event.update.message.from_user.id} not found")
        return True

    logger.exception(f"Update: {event.update}\nException: {event.exception}")
    return True
