from aiogram import Bot
from aiogram.types import BotCommandScopeAllPrivateChats

from app.core.enums import Command


async def setup(bot: Bot) -> None:
    commands = [Command.START.value]
    await bot.set_my_commands(commands=commands, scope=BotCommandScopeAllPrivateChats())


async def delete(bot: Bot) -> None:
    await bot.delete_my_commands(scope=BotCommandScopeAllPrivateChats())
