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
