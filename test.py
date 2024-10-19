# from MySQLdb import _mysql
# import time

# mydb = _mysql.connect(host = "localhost", user="root", password = 'My_sql_2305', database = 'sakila')

# print(mydb.get_server_info())
# time.sleep(10)
import secrets

# Генерация строки соли длиной 32 символа
salt = secrets.token_hex(16)  # вернёт 32-символьную строку
print(salt)
