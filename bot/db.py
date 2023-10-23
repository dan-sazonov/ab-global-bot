import os

from models import models_list, db
import config


def _has_db() -> bool:
    return os.path.isfile(config.DB_FILE)


def _add_words() -> None:
    pass


def create_tables():
    db_prev_state = _has_db()

    with db:
        db.create_tables(models_list)

    if not db_prev_state:
        _add_words()
