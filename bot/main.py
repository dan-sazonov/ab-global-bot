import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message

import config
import messages

dp = Dispatcher()
bot = Bot(config.settings.bot_token, parse_mode=ParseMode.HTML)


@dp.startup()
async def on_startup():
    # await config.set_commands(dp)
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
    await message.answer(messages.START)


@dp.message(Command("help"))
async def command_help_handler(message: Message) -> None:
    await message.answer(messages.HELP)


@dp.message()
async def unknown_command_handler(message: Message) -> None:
    await message.answer(messages.UNKNOWN)


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
