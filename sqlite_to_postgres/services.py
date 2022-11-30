from typing import List


def data_to_dict_via_dataclass(sql_table: dict,
                               table_name: str,
                               table_fetchall_data: list) -> List:
    """ возвращает список объектов Dataclass."""

    result_table_data = []
    for table_data_item in table_fetchall_data:

        dataclass_name = sql_table[table_name]
        dataclass_obj = dataclass_name(*table_data_item)
        result_table_data.append(dataclass_obj)

    return result_table_data


if __name__ == '__main__':
    pass
