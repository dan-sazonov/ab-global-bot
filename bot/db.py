from models import models_list, db


def _has_db() -> bool:
    pass


def _add_words() -> None:
    pass


def create_tables():
    db_prev_state = _has_db()

    with db:
        db.create_tables(models_list)

    if not db_prev_state:
        _add_words()
