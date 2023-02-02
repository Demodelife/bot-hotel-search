from peewee import *
from os import path

db = SqliteDatabase(path.join('database', 'search_history.db'))


class User(Model):
    name = CharField()
    userID = IntegerField()
    command = CharField()
    time = DateTimeField()

    class Meta:
        database = db


class HotelLowPrice(Model):

    owner = ForeignKeyField(User, related_name='hotels_lp')
    city = CharField()
    name = CharField()
    price = CharField()

    class Meta:
        database = db


class HotelHighPrice(Model):

    owner = ForeignKeyField(User, related_name='hotels_hp')
    city = CharField()
    name = CharField()
    price = CharField()

    class Meta:
        database = db


class HotelBestDeal(Model):

    owner = ForeignKeyField(User, related_name='hotels_bd')
    city = CharField()
    name = CharField()
    price = CharField()
    distance = CharField()

    class Meta:
        database = db


db.create_tables([User, HotelLowPrice, HotelHighPrice, HotelBestDeal])
