import logging

from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
from aiogram_dialog import setup_dialogs

from app.bot import middlewares
from app.bot.routers import bot_routers_include
from app.core.config import Config

config = Config.get()
logger = logging.getLogger(__name__)


key_builder = DefaultKeyBuilder(with_destiny=True)
storage = RedisStorage.from_url(url=config.redis.dsn(), key_builder=key_builder)
# storage = MemoryStorage()
dispatcher = Dispatcher(storage=storage)


default_bot_properties = DefaultBotProperties(parse_mode=ParseMode.HTML)
bot = Bot(token=config.bot.TOKEN.get_secret_value(), default=default_bot_properties)
router = Router()


async def setup_dispatcher(dispatcher: Dispatcher) -> None:
    logger.info(f"Dev ID: {config.bot.DEV_ID}")
    dispatcher.include_router(router)
    bot_routers_include(dispatcher)
    setup_dialogs(dispatcher)
    middlewares.register(dispatcher)


async def start_pooling() -> None:
    await setup_dispatcher(dispatcher)
    await dispatcher.start_polling(bot, skip_updates=True)


async def setup_webhook() -> None:
    await setup_dispatcher(dispatcher)
    await bot.set_webhook(
        url=config.bot.WEBHOOK_URL,
        secret_token=config.bot.SECRET_TOKEN.get_secret_value(),
        drop_pending_updates=True,
    )


async def delete_webhook() -> None:
    await bot.delete_webhook()
