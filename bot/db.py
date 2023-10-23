from models import models_list, db, Word, prev_state


def _add_words() -> None:
    pass


def create_tables():
    has_db = prev_state

    with db:
        db.create_tables(models_list)

    if not has_db:
        _add_words()
