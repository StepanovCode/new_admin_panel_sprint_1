import logging
import sqlite3

from data import SQLITE_TABLE_MOVIES
from services import extract_tables_name_sqlite, data_to_dict_via_dataclass


class Extractor:
    def extract_movies(self):
        raise NotImplementedError('Функция extract_movies не'
                                  'переопределена в дочернем классе')


class DataExtractor:
    def __init__(self, db: Extractor):
        self.db = db

    def extract(self):
        return self.db.extract_movies()


class SQLiteExtractor(Extractor):
    def __init__(self, connection: sqlite3.Connection):
        self.conn = connection
        self.cur = None
        self.list_name_tables = []
        self.extract_data_ok = False
        self.data = []
        self.dict_table_movies = {}

    def extract_movies(self) -> dict:
        logging.info('Началась выгрузка данных из Sqlite...')
        self.list_name_tables = extract_tables_name_sqlite(self.conn)
        logging.info(
            f'Список имен таблиц в Sqlite: '
            f'{self.list_name_tables}'
        )
        self.extract_data_ok = self.extract_data()
        if not self.extract_data_ok:
            logging.error('extractor.py -> SQLiteExtractor.extract_movies : '
                          'Выгрузка прервана'
                          )
            return {}
        logging.info(
            'Выгрузка из Sqlite завершена'
        )
        return self.dict_table_movies

    def extract_data(self) -> bool:
        try:
            if self.list_name_tables:
                self.cur = self.conn.cursor()

                for table_name in self.list_name_tables:
                    logging.info(
                        f'Выгрузка данных из таблицы: {table_name}'
                    )
                    self.cur.execute(f'SELECT * FROM {table_name}')
                    self.data = self.cur.fetchall()

                    data = data_to_dict_via_dataclass(
                        SQLITE_TABLE_MOVIES, table_name, self.data)

                    self.dict_table_movies[table_name] = data
                    logging.info(
                        f'Данные из таблицы {table_name} - выгружены'
                    )
                return True
        except Exception as _ex:
            logging.error(
                f'extractor.py -> SQLiteExtractor.extract_data : {_ex}'
            )
            return False


if __name__ == '__main__':
    pass
