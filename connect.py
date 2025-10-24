from ctypes import c_ushort

import psycopg2
from psycopg2.extras import DictCursor #для обращения к ключам
conn = psycopg2.connect(
    host = "127.0.0.1",
    user = "postgres",
    password="",
    port= 5432,
    dbname="db_tg"
)

if conn:
    print("Подключено")

cursor = conn.cursor(cursor_factory=DictCursor)

#добавление в бд

# name = input("Введите заголовок: ")
# height = input("Введите рост: ")
# weight = input("Введите вес: ")
# sql = f"INSERT INTO users(name, height, weight) VALUES('{name}', '{height}', '{weight}');"
# cursor.execute(sql)
# conn.commit()

#второй способ передачи аргументов

name = input("Введите заголовок: ")
height = input("Введите рост: ")
weight = input("Введите вес: ")
sql = f"INSERT INTO users(name, height, weight) VALUES(%s, %s, %s)"
cursor.execute(sql, (name, height, weight))
conn.commit()


cursor.execute("SELECT * FROM users")
result = cursor.fetchall()
print((result[0][1]))
for x in result:
    print(x)
    print(x['name'])

cursor.close()
conn.close()