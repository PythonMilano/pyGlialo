# -*- coding=utf-8 -*-

# from playhouse.migrate import migrate

from models import Pythonista
from dbconn import database_proxy  # , migrator

MODELS = [
    Pythonista,
]


def create_tables():
    database_proxy.connect()
    database_proxy.create_tables(MODELS, safe=True)
    database_proxy.close()


if __name__ == '__main__':
    create_tables()
