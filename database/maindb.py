import sqlite3

db_path = r'database/abbys_db.db'
# db_path = r'abbys_db.db'


def create_table():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS users(
           id INTEGER PRIMARY KEY,
           abbys_status INTEGER DEFAULT(1)
        )""")
    conn.commit()
    conn.close()


def check_user(user_id: int) -> bool:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    sql_request = 'SELECT * FROM users WHERE id=?'
    data = (user_id,)
    cursor.execute(sql_request, data)
    existing_user = cursor.fetchone()
    conn.close()
    return bool(existing_user)


def reg_user(user_id: int):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    if not check_user(user_id):
        sql_request = 'INSERT INTO users(id) VALUES(?)'
        data = (user_id,)
        cursor.execute(sql_request, data)
    conn.commit()
    conn.close()


def get_abbys_status(user_id: int) -> bool:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    sql_request = 'SELECT abbys_status from users where id=?'
    data = (user_id,)
    cursor.execute(sql_request, data)
    status = cursor.fetchone()
    conn.close()
    return status


def update_abbys_status(user_id: int, status: int) -> None:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    sql_request = 'UPDATE users SET abbys_status=? WHERE id=?'
    data = (status, user_id)
    cursor.execute(sql_request, data)
    conn.commit()
    conn.close()


def get_all_id():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM users')
    column_data = cursor.fetchall()
    conn.close()
    return column_data


create_table()
