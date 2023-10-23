from models import models_list, db


def _create_db():
    # only for tests
    with db:
        db.create_tables(models_list)


_create_db()
