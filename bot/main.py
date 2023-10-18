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


@dp.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(messages.START)


@dp.message(Command("help"))
async def command_help_handler(message: Message) -> None:
    await message.answer(messages.HELP)


@dp.message(Command("stop"))
async def command_stop_handler(message: Message) -> None:
    await message.answer(messages.STOP)


async def main() -> None:
    bot = Bot(config.settings.bot_token, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
