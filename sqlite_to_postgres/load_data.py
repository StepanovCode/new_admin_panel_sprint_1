import logging
import sqlite3
import psycopg2

from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
from contextlib import contextmanager

from config import dsl, sqlite_path
from extractor import SQLiteExtractor
from saver import PostgresSaver


@contextmanager
def conn_context(db_path: str):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    sqlite_extractor = SQLiteExtractor(connection)
    postgres_saver = PostgresSaver(pg_conn)

    sqlite_extractor.extract_movies()
    for data in sqlite_extractor.extract_movies():
        if data:
            postgres_saver.save_all_data(data)

    logging.info(
        'Передача данных завершена'
    )


if __name__ == '__main__':

    logging.getLogger()

    with conn_context(sqlite_path) as sqlite_conn, \
            psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
