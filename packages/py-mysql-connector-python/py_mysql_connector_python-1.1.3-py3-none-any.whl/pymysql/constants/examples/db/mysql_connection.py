import pymysql
from pymysql.cursors import DictCursor

# Подключение к БД
connection = pymysql.connect(
    host="localhost",
    user="root",
    password="root",
    database="dbname",
    port=3306,
    cursorclass=DictCursor
)
print("Подключение к MySQL успешно")

def select(query, args=None):
    cursor = connection.cursor()
    try:
        print(query, args if args else "")
        print("*"*40)
        cursor.execute(query, args)
        return cursor.fetchall()
    except Exception as e:
        print(f"Ошибка запроса: {type(e).__name__} {e}")
        raise e
    finally:
        cursor.close()

def update(query, args=None):
    cursor = connection.cursor()
    try:
        print(query, args if args else "")
        print("*"*40)
        cursor.execute(query, args)
        connection.commit()
        return cursor.lastrowid
    except Exception as e:
        print(f"Ошибка запроса: {type(e).__name__} {e}")
        connection.rollback()
        raise e
    finally:
        cursor.close()