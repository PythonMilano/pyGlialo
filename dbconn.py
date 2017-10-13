# -*- coding=utf-8 -*-

import os

from peewee import Proxy

database_proxy = Proxy()
migrator = None

if os.environ['FLASK_DEBUG']:
    from peewee import SqliteDatabase
    from playhouse.migrate import SqliteMigrator

    db = SqliteDatabase(os.environ["DATABASE_URL"])
    migrator = SqliteMigrator(db)
else:
    from urllib import parse
    from peewee import PostgresqlDatabase
    from playhouse.migrate import PostgresqlMigrator

    parse.uses_netloc.append("postgres")
    url = parse.urlparse(os.environ["DATABASE_URL"])

    db = PostgresqlDatabase(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    migrator = PostgresqlMigrator(db)

database_proxy.initialize(db)
