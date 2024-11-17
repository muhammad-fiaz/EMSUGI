import sqlite3

from modules.db import get_db_connection


def init_db():
    """
    Initializes the database by creating necessary tables if they do not exist.
    This function connects to the SQLite database '../../disaster_alerts.db' and creates
    three tables: alerts, current_alerts, and gemini_reports.

    Tables:
    - alerts: Stores historical alert data.
    - current_alerts: Stores the latest fetched alerts.
    - gemini_reports: Stores generated reports.

    Each table is created with the following columns:
    - id: An auto-incrementing primary key.
    - title: The title of the alert or report.
    - link: A unique link to the alert.
    - country: The country associated with the alert.
    - summary: A summary of the alert.
    - keywords: Keywords associated with the alert.
    - tags: Tags associated with the alert.
    - date: The timestamp when the alert or report was created.
    - report: The generated report (only in gemini_reports table).
    - created_at: The timestamp when the report was created (only in gemini_reports table).
    - priority: The priority level of the alert or report (e.g., low, medium, high).
    """
    conn = get_db_connection()
    c = conn.cursor()

    # Create the alerts records table if it does not exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            link TEXT UNIQUE,
            country TEXT,
            summary TEXT,
            keywords TEXT,
            tags TEXT,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Add date column
            priority TEXT  -- Add priority column (TEXT for "low", "medium", "high")
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
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Add date column
            priority TEXT  -- Add priority column (TEXT for "low", "medium", "high")
        )
    ''')

    # Create the gemini_reports table to store generated reports
    c.execute('''
        CREATE TABLE IF NOT EXISTS gemini_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            report TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            priority TEXT  -- Add priority column for reports
        )
    ''')

    conn.commit()
    conn.close()

