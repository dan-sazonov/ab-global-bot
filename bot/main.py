import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, BotCommand, BotCommandScopeDefault
from aiogram import F
from aiogram.utils.markdown import hbold

import config
import messages
import db
from bot import services
from keyboards import keyboard_voting, keyboard_start

dp = Dispatcher()
bot = Bot(config.settings.bot_token, parse_mode=ParseMode.HTML)


async def _set_commands(target: Bot):
    commands = [
        BotCommand(
            command='start',
            description=messages.COMMAND_START
        ),
        BotCommand(
            command='help',
            description=messages.COMMAND_HELP
        )
    ]

    await target.set_my_commands(commands, BotCommandScopeDefault())


class Answer(StatesGroup):
    prev_id = State()


def _new_pair(ids: tuple[int, int]) -> str:
    out = db.get_words(ids)
    return f'{messages.VOTING_TITLE}\n' \
           f'1. {hbold(out[0])}\n\n' \
           f'2. {hbold(out[1])}'


def _parse_state_data(data: dict) -> list[int] | list:
    try:
        ans = data['prev_id'].split('|')
        return [int(i) for i in ans]
    except KeyError:
        return []


def _get_usr_ans(message: Message, ans: list[int]) -> int:
    if message.text.isdecimal() and ans:
        index = int(message.text) - 1
        return ans[index]
    return 0


def _update_counters(message: Message, ids: list[int, int]) -> None:
    if not ids:
        return

    for i in ids:
        db.update_show_num(i)
    db.update_user(message.from_user.id, message.date)


@dp.startup()
async def on_startup():
    db.create_tables()
    await _set_commands(bot)
    await bot.send_message(chat_id=config.settings.admin_id, text=messages.ON_START)


@dp.shutdown()
async def on_shutdown():
    await bot.close()
    await bot.send_message(chat_id=config.settings.admin_id, text=messages.ON_STOP)


@dp.message((F.text == "1") | (F.text == "2") | (F.text == messages.KB_START_TEXT))
async def polling_handler(message: Message, state: FSMContext) -> None:
    data = _parse_state_data(await state.get_data())
    _update_counters(message, data)
    voted_id = _get_usr_ans(message, data)
    db.update_voted_word(voted_id)

    ids = services.get_words_ids()
    await state.update_data(prev_id=f'{ids[0]}|{ids[1]}')
    ans = _new_pair(ids)
    await message.answer(ans, reply_markup=keyboard_voting)


@dp.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    db.add_user(message.from_user.id, message.date)
    await message.answer(messages.START, reply_markup=keyboard_start)


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
