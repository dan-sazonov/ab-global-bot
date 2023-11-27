from datetime import datetime

import services
from models import models_list, db, Word, User, prev_state


def _add_words() -> None:
    """
    Сохраняет в бд words подготовленные модели

    :return: None
    """
    with db:
        Word.insert_many(services.get_words_objects()).execute()


def create_tables() -> None:
    """
    Создает файл с бд, заполняет таблицу со словами

    :return: None
    """
    has_db = prev_state

    with db:
        db.create_tables(models_list)

    if not has_db:
        _add_words()


def add_user(usr_id: int, usr_date: datetime = None) -> None:
    """
    Добавляет юзера в бд

    :param usr_id: тг-ид юзера
    :param usr_date: время его регистрации в боте
    :return: None
    """
    usr_date = usr_date if usr_date else datetime.now()

    usr_obj = User(
        tg_id=usr_id,
        date_reg=usr_date,
        resp_num=0
    )

    query = User.select().where(User.tg_id == usr_id)  # change to EAFP way
    with db:
        if not query.exists():
            usr_obj.save()


def update_user(usr_id: int, usr_date: datetime = None) -> None:
    """
    Обновляет для юзера время активности и инкриминирует количество сообщений

    :param usr_id: тг-ид юзера
    :param usr_date: время последней активности. Если None, будет сохранено текущее
    :return: None
    """
    usr = User.get(User.tg_id == usr_id)
    usr.date_act = usr_date if usr_date else datetime.now()
    usr.resp_num += 1

    with db:
        usr.save()


def update_show_num(word_id: int) -> None:
    """
    Обновляет счетчик показа слова

    :param word_id: ид слова
    :return: None
    """
    word = Word.get(Word.id == word_id)
    word.show_num += 1

    with db:
        word.save()


def update_voted_word(voted_word_id: int) -> None:
    """
    Обновляет счетчик слова, за которое проголосовал юзер

    :param voted_word_id: ид слова
    :return: None
    """
    if not voted_word_id:
        return

    voted_word = Word.get(Word.id == voted_word_id)
    voted_word.vote_num += 1

    with db:
        voted_word.save()


def get_words(words_ids: tuple[int, int]) -> tuple[str]:
    """
    Дергает из бд два слова по их идам

    :param words_ids: иды слов, кортеж
    :return: кортеж самих слов
    """
    out = []

    for i in words_ids:
        out.append(str(Word.get(Word.id == i).word))

    return tuple(out)
