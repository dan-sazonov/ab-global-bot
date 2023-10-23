import peewee as pw

db = pw.SqliteDatabase('data.db')


class BaseModel(pw.Model):
    class Meta:
        database = db


class User(BaseModel):
    id = pw.PrimaryKeyField(unique=True)
    tg_id = pw.BigIntegerField(unique=True)
    date_reg = pw.DateTimeField()
    date_act = pw.DateTimeField()
    resp_num = pw.IntegerField()

    class Meta:
        db_table = 'users'
        order_by = 'resp_num'


class Word(BaseModel):
    id = pw.PrimaryKeyField(unique=True)
    word = pw.CharField()
    show_num = pw.IntegerField()
    vote_num = pw.IntegerField()

    class Meta:
        db_table = 'words'


def _create_db():
    # only for tests
    with db:
        db.create_tables([User, Word])


_create_db()
