import sqlite3

# connection = sqlite3.connect('verifybot.db')
# cursor = connection.cursor()


def create_table_banned_users():
    with sqlite3.connect('verifybot.db') as connection:
        cursor = connection.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Banned_Users
        (telegram_user_id INT,
        username VARCHAR(35))
        ''')


def read_table_banned_users():
    with sqlite3.connect('verifybot.db') as connection:
        cursor = connection.cursor()
        records = cursor.execute("SELECT * FROM Banned_Users")
        return records.fetchall()


def insert_banned_user(telegram_user_id, username):
    with sqlite3.connect('verifybot.db') as connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO Banned_Users VALUES(?, ?)", (telegram_user_id, username))
        connection.commit()


def check_in_ban_list(telegram_user_id):
    with sqlite3.connect('verifybot.db') as connection:
        cursor = connection.cursor()
        banned_user = cursor.execute("SELECT * FROM Banned_Users WHERE telegram_user_id=?", (telegram_user_id,))
        return bool(banned_user.fetchall())
