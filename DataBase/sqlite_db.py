import sqlite3 as sq
from createbot import *
import datetime
from loggers import database_logger


def sql_start():
    global base, cur

    base = sq.connect('DataBase/database.db')
    cur = base.cursor()
    if base:
        database_logger.info('База данных подключена')

    base.execute('CREATE TABLE IF NOT EXISTS Users(user_id BINDING PRIMARY KEY, username TEXT, register_date DATETIME)')
    base.commit()
    base.execute('CREATE TABLE IF NOT EXISTS Messages(message_id BINDING PRIMARY KEY, recipient BINDING, sender BINDING, content TEXT, register_date DATETIME)')
    base.commit()
    base.execute('CREATE TABLE IF NOT EXISTS Payments(payment_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, payer BINDING, currency TEXT, amount INTEGER, register_date DATETIME)')
    base.commit()



async def sql_add_id(message) -> None:
    id_user = message.from_user.id
    username = message.from_user.username
    if (id_user,) not in cur.execute('SELECT user_id FROM Users').fetchall():
        current_timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        base.execute('INSERT INTO Users (user_id, username, register_date) VALUES (?, ?, ?)', (id_user, username, current_timestamp))
        base.commit()
        database_logger.info(f"Пользователь {id_user}-{username} добавлен в базу данных.")


async def sql_add_message(message, content, recipient_id) -> None:
    user_id = message.from_user.id
    msg_id = message.message_id
    current_timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    base.execute('INSERT INTO Messages (message_id, recipient, sender, content, register_date) VALUES (?, ?, ?, ?, ?)', (msg_id, recipient_id, user_id, content, current_timestamp))
    base.commit()
    database_logger.info(f"Сообщение {msg_id} добавлено в базу данных. Маршрут сообщения от {user_id} -> {recipient_id}")


async def sql_add_payment(payer_id, currency, amount):
    current_timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    base.execute('INSERT INTO Payments (payer, currency, amount, register_date) VALUES (?, ?, ?, ?)', (payer_id, currency, amount, current_timestamp))
    base.commit()


async def sql_select_id(username):
    user_id = cur.execute('SELECT user_id FROM Users WHERE username = (?)', (username, )).fetchone()
    return user_id


async def sql_select_username(user_id):
    username = cur.execute('SELECT username FROM Users WHERE user_id = (?)', (user_id, )).fetchone()
    return username