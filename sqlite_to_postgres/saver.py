import logging
from dataclasses import astuple
from data import SequenceSqlTableSaver
from psycopg2.extensions import connection as _connection
from psycopg2 import sql
from psycopg2.extras import execute_values


class Saver:
    def save_all_data(self, data: dict):
        raise NotImplementedError('Функция save_all_data не'
                                  'переопределена в дочернем классе')


class DataSaver:
    def __init__(self, db):
        self.db = db

    def saver(self, data: dict):
        return self.db.save_all_data(data)


class PostgresSaver(Saver):
    def __init__(self, connection: _connection):
        self.conn = connection
        self.cur = None
        self.data = None

    def save_all_data(self, data: dict):
        try:
            self.cur = self.conn.cursor()
            for seq in SequenceSqlTableSaver:
                query = sql.SQL(
                    "INSERT INTO content.{seq_name}"
                    "VALUES %s"
                    "ON CONFLICT (id) DO NOTHING;"
                ).format(seq_name=sql.Identifier(seq.name))
                param = [astuple(value) for value in data[seq.name]]
                execute_values(self.cur, query, param)
                self.conn.commit()
                logging.info(
                    f'Данные таблицы: {seq.name} загружены в таблицу Postgres'
                )
            return 'Копирование данных завершено'
        except Exception as _ex:
            logging.error(f'saver.py -> PostgresSaver.save_all_data : {_ex}')
            return 'Копирование данных прервано'
