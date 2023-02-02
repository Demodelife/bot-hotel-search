from peewee import *
from os import path

db = SqliteDatabase(path.join('database', 'search_history.db'))


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


db.create_tables([User, HotelLowPrice, HotelHighPrice, HotelBestDeal])
