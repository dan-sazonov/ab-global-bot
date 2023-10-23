from models import models_list, db, Word, prev_state
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
