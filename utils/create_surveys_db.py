from peewee import *
from os import path

db = SqliteDatabase(path.join('database', 'surveys.db'))


class Person(Model):
    """Класс БД: Пользователь опросника"""

    date = DateTimeField()
    userID = IntegerField()
    name = CharField()
    age = IntegerField()
    country = CharField()
    city = CharField()
    phone_number = IntegerField(default='No')

    class Meta:
        database = db


db.create_tables([Person])
