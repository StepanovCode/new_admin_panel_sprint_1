import logging
import sqlite3
from typing import Generator
from data import SQLITE_TABLE_MOVIES, SequenceSqlTableSaver
from services import data_to_dict_via_dataclass


class Extractor:
    def extract_movies(self):
        raise NotImplementedError('Функция extract_movies не'
                                  'переопределена в дочернем классе')


class SQLiteExtractor(Extractor):
    def __init__(self, connection: sqlite3.Connection):
        self.conn = connection
        self.cur = None
        self.data = []
        self.dict_table_movies = {}

    def extract_movies(self) -> Generator[dict, None, None]:
        logging.info('Началась выгрузка данных из Sqlite...')

        try:
            self.cur = self.conn.cursor()
            for table_name in SequenceSqlTableSaver:
                logging.info(
                    f'Выгрузка данных из таблицы: {table_name.name}'
                )

                self.cur.execute(f'SELECT * FROM {table_name.name}')
                while True:
                    self.dict_table_movies = {}
                    self.data = self.cur.fetchmany(10000)
                    if not self.data:
                        break

                    data = data_to_dict_via_dataclass(
                        SQLITE_TABLE_MOVIES, table_name.name, self.data)

                    self.dict_table_movies[table_name.name] = data

                    yield self.dict_table_movies

            logging.info(
                'Данные выгружены из Sqlite'
            )

        except Exception as _ex:
            logging.error(
                f'extractor.py -> SQLiteExtractor.extract_data : {_ex}'
            )


if __name__ == '__main__':
    pass
