import sqlite3


def init_db():
    conn = sqlite3.connect('disaster_alerts.db')
    c = conn.cursor()

    # Create the alerts history table if it does not exist
    c.execute(''' 
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            link TEXT UNIQUE,
            country TEXT,
            summary TEXT,
            keywords TEXT,
            tags TEXT,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Add date column
        )
    ''')

    # Create the current alerts table for the latest fetched alerts
    c.execute('''
        CREATE TABLE IF NOT EXISTS current_alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            link TEXT UNIQUE,
            country TEXT,
            summary TEXT,
            keywords TEXT,
            tags TEXT,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Add date column
        )
    ''')

    # Create the gemini_reports table to store generated reports
    c.execute('''
        CREATE TABLE IF NOT EXISTS gemini_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            report TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()
