import os

from peewee import Model, PrimaryKeyField, BigIntegerField, DateTimeField, IntegerField, CharField, SqliteDatabase
import config

prev_state = os.path.isfile(config.DB_FILE)
db = SqliteDatabase(config.DB_FILE)


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    id = PrimaryKeyField(unique=True)
    tg_id = BigIntegerField(unique=True)
    date_reg = DateTimeField()
    date_act = DateTimeField()
    resp_num = IntegerField()

    class Meta:
        db_table = 'users'
        order_by = 'resp_num'


class Word(BaseModel):
    id = PrimaryKeyField(unique=True)
    word = CharField(max_length=100)
    show_num = IntegerField()
    vote_num = IntegerField()

    class Meta:
        db_table = 'words'


models_list = [User, Word]
