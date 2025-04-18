import sqlite3

def get_connection():
    return sqlite3.connect('library.db')

def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT,
            year INTEGER,
            genre TEXT,
            read BOOLEAN
        )
    ''')
    conn.commit()
    conn.close()
