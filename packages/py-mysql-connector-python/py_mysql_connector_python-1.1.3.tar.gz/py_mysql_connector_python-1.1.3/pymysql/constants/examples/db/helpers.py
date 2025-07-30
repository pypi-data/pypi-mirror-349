from db.mysql_connection import select

from settings import settings


def get_columns(table_name):
    query = ("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS \n"
             "WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s \n"
             "ORDER BY ORDINAL_POSITION;")
    result_dict = select(query, (settings.db_name, table_name))

    return [row["COLUMN_NAME"] for row in result_dict]

def get_column_info(table_name, column_name):
    query = ("SELECT * FROM INFORMATION_SCHEMA.COLUMNS \n"
             "WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s AND COLUMN_NAME = %s \n"
             "ORDER BY ORDINAL_POSITION;")
    result_tuple = select(query, (settings.db_name, table_name, column_name))

    return result_tuple[0]


def get_foreign_key_info(table_name, column_name):
    query = ("SELECT REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME \n"
            "FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE \n"
            "WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s \n"
            "AND COLUMN_NAME = %s AND REFERENCED_TABLE_NAME IS NOT NULL;")
    result_dict = select(query, (settings.db_name, table_name, column_name))
    if result_dict:
        result_dict = result_dict[0]

    return result_dict["REFERENCED_TABLE_NAME"], result_dict["REFERENCED_COLUMN_NAME"]

