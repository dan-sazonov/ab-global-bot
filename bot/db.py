from datetime import datetime

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

    with db:
        usr_obj.save()


def update_user(usr_id: int, usr_date: datetime = None):
    usr = User.get(User.tg_id == usr_id)
    usr.date_act = usr_date if usr_date else datetime.now()
    usr.resp_num = usr.resp_num + 1

    with db:
        usr.save()


def update_words(voted_word_id: int, linked_word_id: int):
    voted_word = Word.get(Word.id == voted_word_id)
    voted_word.show_num += 1
    voted_word.vote_num += 1

    linked_word = Word.get(Word.id == linked_word_id)
    linked_word.show_num += 1

    with db:
        voted_word.save()
        linked_word.save()
