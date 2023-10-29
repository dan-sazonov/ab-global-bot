from datetime import datetime

from peewee import fn

from models import models_list, db, Word, User, prev_state
import services


def _add_words() -> None:
    with db:
        Word.insert_many(services.get_words_objects()).execute()


def create_tables():
    has_db = prev_state

    with db:
        db.create_tables(models_list)

    if not has_db:
        _add_words()


def add_user(usr_id: int, usr_date: datetime = None):
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


def update_user(usr_id: int, usr_date: datetime = None):
    usr = User.get(User.tg_id == usr_id)
    usr.date_act = usr_date if usr_date else datetime.now()
    usr.resp_num += 1

    with db:
        usr.save()


def _update_show_num(word_id: int) -> None:
    word = Word.get(Word.id == word_id)
    word.show_num += 1

    with db:
        word.save()


def update_voted_word(voted_word_id: int):
    if not voted_word_id:
        return

    voted_word = Word.get(Word.id == voted_word_id)
    voted_word.vote_num += 1

    with db:
        voted_word.save()


def get_words(words_ids: tuple[int, int]) -> tuple[str]:
    out = []

    for i in words_ids:
        _update_show_num(i)
        out.append(str(Word.get(Word.id == i).word))

    return tuple(out)
