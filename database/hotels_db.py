from peewee import SqliteDatabase, Model, CharField, IntegerField, DateTimeField, ForeignKeyField
from os import path

db = SqliteDatabase(path.join('database', 'users.db'))


class User(Model):
    """Класс БД: Пользователь"""

    name = CharField()
    userID = IntegerField()
    command = CharField()
    time = DateTimeField()

    class Meta:
        database = db


class HotelLowPrice(Model):
    """Класс БД: Отели команды /lowprice"""

    owner = ForeignKeyField(User, related_name='hotels_lp')
    city = CharField()
    name = CharField()
    price = CharField()

    class Meta:
        database = db


class HotelHighPrice(Model):
    """Класс БД: Отели команды /highprice"""

    owner = ForeignKeyField(User, related_name='hotels_hp')
    city = CharField()
    name = CharField()
    price = CharField()

    class Meta:
        database = db


class HotelBestDeal(Model):
    """Класс БД: Отели команды /bestdeal"""

    owner = ForeignKeyField(User, related_name='hotels_bd')
    city = CharField()
    name = CharField()
    price = CharField()
    distance = CharField()

    class Meta:
        database = db


class PersonSurvey(Model):
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


tables = [User, HotelLowPrice, HotelHighPrice, HotelBestDeal, PersonSurvey]
