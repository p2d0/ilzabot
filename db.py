import sqlite3

def setup_database():
    conn = sqlite3.connect('messages.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS messages (message_id INTEGER PRIMARY KEY, user_id INTEGER)''')
    conn.commit()
    return conn

def store_message(conn, message_id, user_id):
    c = conn.cursor()
    c.execute('INSERT INTO messages (message_id, user_id) VALUES (?, ?)', (message_id, user_id))
    conn.commit()

def get_user_id_by_message_id(conn, message_id):
    c = conn.cursor()
    c.execute('SELECT user_id FROM messages WHERE message_id=?', (message_id,))
    result = c.fetchone()
    if result is not None:
        return result[0]
    else:
        return None
