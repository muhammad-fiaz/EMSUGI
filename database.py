import sqlite3


def init_db():
    conn = sqlite3.connect('disaster_alerts.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            link TEXT UNIQUE,
            country TEXT,
            summary TEXT,
            keywords TEXT,
            tags TEXT
        )
    ''')
    conn.commit()
    conn.close()
