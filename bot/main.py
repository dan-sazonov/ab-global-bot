import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message

import config
import messages
import db
from bot import services

dp = Dispatcher()
bot = Bot(config.settings.bot_token, parse_mode=ParseMode.HTML)


@dp.startup()
async def on_startup():
    db.create_tables()
    await bot.send_message(chat_id=config.settings.admin_id, text=messages.ON_START)


@dp.shutdown()
async def on_shutdown():
    await bot.close()
    await bot.send_message(chat_id=config.settings.admin_id, text=messages.ON_STOP)


@dp.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    db.add_user(message.from_user.id, message.date)
    await message.answer(messages.START)


@dp.message(Command("help"))
async def command_help_handler(message: Message) -> None:
    await message.answer(messages.HELP)


@dp.message(Command("test"))
async def command_help_handler(message: Message) -> None:
    ids = services.get_words_ids()
    out = db.get_words(ids)
    db.update_user(message.from_user.id, message.date)
    await message.answer(f'{out[0]}, {out[1]}')


@dp.message()
async def unknown_command_handler(message: Message) -> None:
    await message.answer(messages.UNKNOWN)


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
