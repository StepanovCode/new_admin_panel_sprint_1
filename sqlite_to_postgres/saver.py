import logging
from dataclasses import astuple
from psycopg2 import sql
from psycopg2.extensions import connection as _connection
from psycopg2.extras import execute_values


class Saver:
    def save_all_data(self, data: dict):
        raise NotImplementedError('Функция save_all_data не'
                                  'переопределена в дочернем классе')


class PostgresSaver(Saver):
    def __init__(self, connection: _connection):
        self.conn = connection
        self.cur = None
        self.data = None

    def save_all_data(self, data: dict):
        try:
            self.cur = self.conn.cursor()
            for table_name in data.keys():
                query = sql.SQL(
                    "INSERT INTO content.{seq_name}"
                    "VALUES %s"
                    "ON CONFLICT (id) DO NOTHING;"
                ).format(seq_name=sql.Identifier(table_name))
                param = [astuple(value) for value in data[table_name]]
                execute_values(self.cur, query, param)

                self.conn.commit()

                logging.info(
                    f'Данные таблицы: {table_name}'
                    f'загружены в таблицу Postgres'
                )

        except Exception as _ex:
            logging.error(f'saver.py -> PostgresSaver.save_all_data : {_ex}')
