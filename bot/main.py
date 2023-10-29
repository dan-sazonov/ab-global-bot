import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import F
from aiogram.utils.markdown import hbold

import config
import messages
import db
from bot import services
from keyboards import keyboard_voting

dp = Dispatcher()
bot = Bot(config.settings.bot_token, parse_mode=ParseMode.HTML)


def _new_pair(message) -> str:
    ids = services.get_words_ids()
    out = db.get_words(ids)
    db.update_user(message.from_user.id, message.date)
    return f'1. {hbold(out[0])}\n\n' \
           f'2. {hbold(out[1])}'


@dp.startup()
async def on_startup():
    db.create_tables()
    await bot.send_message(chat_id=config.settings.admin_id, text=messages.ON_START)


@dp.shutdown()
async def on_shutdown():
    await bot.close()
    await bot.send_message(chat_id=config.settings.admin_id, text=messages.ON_STOP)


@dp.message((F.text == "1") | (F.text == "2"))
async def polling_handler(message: Message) -> None:
    ans = _new_pair(message)
    await message.answer(ans, reply_markup=keyboard_voting)


#   todo определяем номер цифры
#   todo голосуем за айдишник под указанным номером
#   todo сбрасываем фсм
#   todo показываем новое сообщение
#   todo сохраняем в фсм их айдишники

@dp.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    db.add_user(message.from_user.id, message.date)
    await message.answer(messages.START)

    await polling_handler(message)


@dp.message(Command("help"))
async def command_help_handler(message: Message) -> None:
    await message.answer(messages.HELP)


@dp.message((F.from_user.id == config.settings.admin_id) & (F.text == "test"))
async def command_help_handler(message: Message) -> None:
    await message.answer(_new_pair(message))


@dp.message()
async def unknown_command_handler(message: Message) -> None:
    await message.answer(messages.UNKNOWN)


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
