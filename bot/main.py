import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram import F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, BotCommand, BotCommandScopeDefault
from aiogram.utils.markdown import hbold

import config
import db
import messages
import services
from keyboards import keyboard_voting, keyboard_start

dp = Dispatcher()
bot = Bot(config.settings.bot_token, parse_mode=ParseMode.HTML)


async def _set_commands(target: Bot) -> None:
    """
    Задает список команд бота, вызывается один раз при старте

    :param target: основной объект бота
    :return: None
    """
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
    """Стэйт, в котором сохраняется строка вида 'id_первого_слова|id_второго_слова' """
    prev_id = State()


def _new_pair(ids: tuple[int, int]) -> str:
    """
    Готовит сообщения бота с вариантами названий

    :param ids: кортеж из двух идов
    :return: строка с текстом сообщения
    """
    out = db.get_words(ids)
    return f'{messages.VOTING_TITLE}\n' \
           f'1. {hbold(out[0])}\n\n' \
           f'2. {hbold(out[1])}'


def _parse_state_data(data: dict) -> list[int] | list:
    """
    Парсит строку из стэйта

    :param data: словарь данных стэйта
    :return: лист идов названий из текущего сообщения бота, или пустой список, если это первое сообщение
    """
    try:
        ans = data['prev_id'].split('|')
        return [int(i) for i in ans]
    except KeyError:
        return []


def _get_usr_ans(message: Message, ans: list[int]) -> int:
    """
    Возвращает ид названия, за которое проголосовал пользователь

    :param message: объект сообщения
    :param ans: иды предложенных названий
    :return: ид названия, за которое отдан голос, или ноль
    """
    if message.text.isdecimal() and ans:
        index = int(message.text) - 1
        return ans[index]
    return 0


def _update_counters(message: Message, ids: list[int, int]) -> None:
    """
    Увеличивает счетчик показов для двух названий

    :param message: объект сообщения, из него нужен только ид пользователя
    :param ids: иды показанных пользователю слов
    :return: None
    """
    if not ids:
        return

    for i in ids:
        db.update_show_num(i)
    db.update_user(message.from_user.id, message.date)


@dp.startup()
async def on_startup():
    """
    По запуску бота - создаем бд, заводим список команд бота, отправляем админу сообщение, что все ок

    :return: None
    """
    db.create_tables()
    await _set_commands(bot)
    await bot.send_message(chat_id=config.settings.admin_id, text=messages.ON_START)


@dp.shutdown()
async def on_shutdown():
    """
    По остановке бота - закрываем луп асинки и пишем админу

    :return: None
    """
    await bot.close()
    await bot.send_message(chat_id=config.settings.admin_id, text=messages.ON_STOP)


@dp.message((F.text == "1") | (F.text == "2") | (F.text == messages.KB_START_TEXT))
async def polling_handler(message: Message, state: FSMContext) -> None:
    """
    Обрабатывает ответ пользователя на голосование или его начало. Вся логика голосования дергается отсюда

    :param message: объект сообщения
    :param state: стэйт, в нем храним ответ пользователя на предыдущее голосование
    :return: None
    """
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
    Отвечает на запуск бота - пригласительное сообщение и клавиатура с текстовой кнопкой начала

    :param message: объект сообщения
    :return: None
    """
    db.add_user(message.from_user.id, message.date)
    await message.answer(messages.START, reply_markup=keyboard_start)


@dp.message(Command("help"))
async def command_help_handler(message: Message) -> None:
    """
    Выводит справочное сообщение по команде /help

    :param message: объект сообщения
    :return: None
    """
    await message.answer(messages.HELP)


@dp.message()
async def unknown_command_handler(message: Message) -> None:
    """
    Обработчик непонятных боту сообщений

    :param message: объект сообщения
    :return: None
    """
    await message.answer(messages.UNKNOWN)


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
