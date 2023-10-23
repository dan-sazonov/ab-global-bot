from models import models_list, db


def create_tables():
    with db:
        db.create_tables(models_list)
