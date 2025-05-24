import logging

from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram_dialog import AccessSettings, DialogManager, ShowMode, StartMode

from app.bot.routers.main_menu.dialog import MainMenuState
from app.core.config import Config

logger = logging.getLogger(__name__)
config = Config.get()
router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message, dialog_manager: DialogManager) -> None:
    logger.info(f"Command /start from {message.from_user.id}")
    dialog_manager.show_mode = ShowMode.DELETE_AND_SEND

    await dialog_manager.start(
        MainMenuState.main_menu,
        mode=StartMode.RESET_STACK,
        access_settings=AccessSettings(user_ids=[config.bot.DEV_ID]),
    )
