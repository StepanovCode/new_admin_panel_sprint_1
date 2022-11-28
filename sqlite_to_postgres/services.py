def extract_tables_name_sqlite(connection):
    """ возвращает список названий таблиц из SQLite."""

    list_name_of_table = []
    cur = connection.cursor()
    cur.execute('SELECT * FROM sqlite_master;')
    cur_data = cur.fetchall()
    [list_name_of_table.append(_[1]) for _ in cur_data if _[0] == 'table']

    return list_name_of_table


def data_to_dict_via_dataclass(sql_table: dict,
                               table_name: str,
                               table_fetchall_data: list):
    """ возвращает список объектов Dataclass."""

    result_table_data = []
    for table_data_item in table_fetchall_data:
        # создаем объект Dataclass из *data_item
        # dataclass_name = dict_of_table[table_key](*data_item)
        dataclass_name = sql_table[table_name]
        dataclass_obj = dataclass_name(*table_data_item)
        result_table_data.append(dataclass_obj)

    return result_table_data


if __name__ == '__main__':
    pass
