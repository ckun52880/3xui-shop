import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from aiogram.types import Update
from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware

from app import bot
from app.core.config import Config
from app.core.constants import HEADER_SECRET_TOKEN

config = Config.get()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(application: FastAPI) -> AsyncGenerator[None, None]:
    logger.info("Starting application")
    await bot.setup_webhook()
    yield
    await bot.delete_webhook()
    logger.info("Stopping application, deleting webhook")


app = FastAPI(
    lifespan=lifespan,
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post(config.bot.WEBHOOK_PATH)
async def webhook(request: Request, update: Update) -> None | dict:
    secret_token = request.headers.get(HEADER_SECRET_TOKEN)

    if not secret_token:
        logger.error("Missing secret token")
        return {"status": "error", "message": "Missing secret token"}

    if secret_token != config.bot.SECRET_TOKEN.get_secret_value():
        logger.error("Wrong secret token")
        return {"status": "error", "message": "Wrong secret token"}

    update = Update.model_validate(await request.json(), context={"bot": bot.bot})
    await bot.dispatcher.feed_webhook_update(bot=bot.bot, update=update)
    return {"ok": True}
