from peewee import Model, PrimaryKeyField, BigIntegerField, DateTimeField, IntegerField, CharField, SqliteDatabase

db = SqliteDatabase('../data.db')


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
    word = CharField()
    show_num = IntegerField()
    vote_num = IntegerField()

    class Meta:
        db_table = 'words'


models_list = [User, Word]
