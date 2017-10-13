# -*- coding=utf-8 -*-

from peewee import Model, CharField, DateTimeField
from dbconn import database_proxy


class BaseModel(Model):
    class Meta:
        database = database_proxy


class Pythonista(BaseModel):
    name = CharField()
    email = CharField()
    eb_id = CharField()
    check_in = DateTimeField()
