import logging
import sqlite3
import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

from extractor import SQLiteExtractor, DataExtractor
from saver import PostgresSaver, DataSaver


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    sqlite_extractor = SQLiteExtractor(connection)
    data = DataExtractor(sqlite_extractor).extract()

    postgres_saver = PostgresSaver(pg_conn)
    done = DataSaver(postgres_saver).saver(data)
    logging.info(done)


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    dsl = {'dbname': 'movies_database',
           'user': 'app',
           'password': '123qwe',
           'host': '127.0.0.1',
           'port': 8090
           }
    with sqlite3.connect('db.sqlite') as sqlite_conn, \
            psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
