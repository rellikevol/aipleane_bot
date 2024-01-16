import sqlite3
from datetime import date
from telegram_bot.globals import global_days_delta


def create_db(name: str):
    conn = sqlite3.connect(name)
    cursr = conn.cursor()
    cursr.execute("""CREATE TABLE IF NOT EXISTS requests(
       user_id INT,
       user_name TEXT, 
       chat_id INT,
       type TEXT,
       point_from_town TEXT,
       point_from_state TEXT,
       point_from_country TEXT,
       point_to_town TEXT,
       point_to_state TEXT,
       point_to_country TEXT,
       description TEXT,
       status TEXT,
       year_create INT,
       month_create INT,
       day_create iNT,
       year INT,
       month INT,
       day iNT,
       price TEXT,
       pk INTEGER PRIMARY KEY AUTOINCREMENT
       );
    """)
    cursr.execute("""CREATE TABLE IF NOT EXISTS messages_for_devs(
           user_id INT,
           user_name TEXT, 
           message INT,
           pk INTEGER PRIMARY KEY AUTOINCREMENT
           );
        """)
    conn.commit()
    cursr.close()
    conn.close()


def insert_devs_message(name, user_id, user_name, message):
    conn = sqlite3.connect(name)
    cursr = conn.cursor()
    cursr.execute("""INSERT INTO messages_for_devs(user_id, user_name, message) 
    VALUES(?, ?, ?);""", (user_id, user_name, message))
    conn.commit()
    cursr.close()
    conn.close()


def insert_send(name, user_id, user_name, chat_id, type, point_from_town, point_from_state, point_from_country,
                point_to_town, point_to_state, point_to_country, description, status,
                year_create, month_create, day_create):
    conn = sqlite3.connect(name)
    cursr = conn.cursor()
    cursr.execute("""INSERT INTO requests(user_id, user_name, chat_id, type, 
    point_from_town, point_from_state, point_from_country, 
    point_to_town, point_to_state, point_to_country,
    description, status, 
    year_create, month_create, day_create) 
    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);""",
                  (user_id, user_name, chat_id, type, point_from_town, point_from_state, point_from_country,
                   point_to_town, point_to_state, point_to_country, description, status,
                   year_create, month_create, day_create))
    conn.commit()
    cursr.close()
    conn.close()


def insert_carry(name, user_id, user_name, chat_id, type,
                 point_from_town, point_from_state, point_from_country,
                 point_to_town, point_to_state, point_to_country,
                 description, status, price, year_create, month_create, day_create,
                 year, month, day):
    conn = sqlite3.connect(name)
    cursr = conn.cursor()
    cursr.execute("""INSERT INTO requests(user_id, user_name, chat_id, type, 
    point_from_town, point_from_state, point_from_country,
    point_to_town, point_to_state, point_to_country, 
    description, status, price, 
    year_create, month_create, day_create, 
    year, month, day) 
    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);""",
                  (user_id, user_name, chat_id, type,
                   point_from_town, point_from_state, point_from_country,
                   point_to_town, point_to_state, point_to_country,
                   description, status, price, year_create, month_create, day_create, year, month, day))
    conn.commit()
    cursr.close()
    conn.close()


def user_tasks(name, user_id):
    conn = sqlite3.connect(name)
    cursr = conn.cursor()
    res = cursr.execute("""SELECT * FROM requests WHERE user_id=?;""", (user_id,)).fetchall()
    conn.commit()
    cursr.close()
    conn.close()
    return res


def user_tasks_send(name, user_id):
    conn = sqlite3.connect(name)
    cursr = conn.cursor()
    res = cursr.execute("""SELECT * FROM requests WHERE user_id=? AND type=?;""", (user_id, 'send')).fetchall()
    conn.commit()
    cursr.close()
    conn.close()
    return res


def user_tasks_carry(name, user_id):
    conn = sqlite3.connect(name)
    cursr = conn.cursor()
    res = cursr.execute("""SELECT * FROM requests WHERE user_id=? AND type=?;""", (user_id, 'carry')).fetchall()
    conn.commit()
    cursr.close()
    conn.close()
    return res


def delete_request(name, pk):
    conn = sqlite3.connect(name)
    cursr = conn.cursor()
    cursr.execute("""DELETE FROM requests WHERE pk=?;""", (pk,))
    conn.commit()
    cursr.close()
    conn.close()


def get_request(name, pk):
    conn = sqlite3.connect(name)
    cursr = conn.cursor()
    res = cursr.execute("""SELECT * FROM requests WHERE pk=?;""", (pk,)).fetchall()
    cursr.close()
    conn.close()
    return res


def all_tasks(name):
    conn = sqlite3.connect(name)
    cursr = conn.cursor()
    res = cursr.execute("""SELECT * FROM tasks;""").fetchall()
    conn.commit()
    cursr.close()
    conn.close()
    return res


def check_date(date: str):
    a = date.split('.')
    if len(a) != 3:
        return False
    for i in a:
        for x in i:
            if not x.isdigit():
                return False
    return True


def date_to_digts(date: str):
    a = date.split('.')
    for i in range(len(a)):
        a[i] = int(a[i])
    return a


def find_carry_in_base(name, user_id):
    conn = sqlite3.connect(name)
    cursr = conn.cursor()
    res = cursr.execute("""SELECT * FROM requests WHERE user_id=? AND type=? AND status=?;""",
                        (user_id, 'send', 'created')).fetchall()
    if len(res) == 0:
        return res
    carry = []
    for i, x in enumerate(res):
        result = cursr.execute("""SELECT * FROM requests 
        WHERE type=? AND status=?
        AND point_from_town=? AND point_from_state=? AND point_from_country=?
        AND point_to_town=? AND point_to_state=? AND point_to_country=? AND user_id!=?;""", ('carry', 'created',
                                                                                             x[4], x[5], x[6],
                                                                                             x[7], x[8], x[9],
                                                                                             user_id)).fetchall()
        if len(result) != 0:
            for n in result:
                if n not in carry:
                    carry.append(n)
    cursr.close()
    conn.close()
    if len(carry) != 0:
        result = []
        for i, x in enumerate(carry):
            today = date.today()
            if x[15] is not None:
                delivery_date = date(x[15], x[16], x[17])
                if today < delivery_date:
                    result.append(x)
            else:
                creation_date = date(x[12], x[13], x[14])
                delta = today - creation_date
                if delta.days <= global_days_delta:
                    result.append(x)
        return result
    else:
        return carry


def find_send_in_base(name, user_id):
    conn = sqlite3.connect(name)
    cursr = conn.cursor()
    res = cursr.execute("""SELECT * FROM requests WHERE user_id=? AND type=? AND status=?;""",
                        (user_id, 'carry', 'created')).fetchall()
    if len(res) == 0:
        return res
    send = []
    for i, x in enumerate(res):
        result = cursr.execute("""SELECT * FROM requests 
            WHERE type=? AND status=?
            AND point_from_town=? AND point_from_state=? AND point_from_country=? 
            AND point_to_town=? AND point_to_state=? AND point_to_country=? AND user_id!=?;""", ('send', 'created',
                                                                                                 x[4], x[5], x[6],
                                                                                                 x[7], x[8], x[9],
                                                                                                 user_id)).fetchall()
        if len(result) != 0:
            for n in result:
                if n not in send:
                    send.append(n)
    cursr.close()
    conn.close()
    if len(send) != 0:
        result = []
        for i, x in enumerate(send):
            today = date.today()
            creation_date = date(x[12], x[13], x[14])
            delta = today - creation_date
            if delta.days <= global_days_delta:
                result.append(x)
        return result
    else:
        return send


def find_send_while_create(name,
                           point_from_town, point_from_state, point_from_country,
                           point_to_town, point_to_state, point_to_country):
    conn = sqlite3.connect(name)
    cursr = conn.cursor()
    result = cursr.execute("""SELECT * FROM requests WHERE type=? AND status=? 
        AND point_from_town=? AND point_from_state=? AND point_from_country=? 
        AND point_to_town=? AND point_to_state=? AND point_to_country=?;""", ('send', 'created',
                                                                              point_from_town, point_from_state,
                                                                              point_from_country,
                                                                              point_to_town, point_to_state,
                                                                              point_to_country)).fetchall()
    send = []
    if len(result) != 0:
        for n in result:
            if n[2] not in send:
                send.append(n[2])
    cursr.close()
    conn.close()
    return send


def find_carry_while_create(name,
                            point_from_town, point_from_state, point_from_country,
                            point_to_town, point_to_state, point_to_country):
    conn = sqlite3.connect(name)
    cursr = conn.cursor()
    result = cursr.execute("""SELECT * FROM requests WHERE type=? AND status=? 
    AND point_from_town=? AND point_from_state=? AND point_from_country=? 
    AND point_to_town=? AND point_to_state=? AND point_to_country=?;""", ('carry', 'created',
                                                                          point_from_town, point_from_state,
                                                                          point_from_country,
                                                                          point_to_town, point_to_state,
                                                                          point_to_country)).fetchall()
    carry = []
    if len(result) != 0:
        for n in result:
            if n[2] not in carry:
                carry.append(n[2])
    cursr.close()
    conn.close()
    return carry
