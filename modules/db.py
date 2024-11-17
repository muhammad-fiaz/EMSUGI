import sqlite3
import os

def get_db_connection():
    """
    Creates and returns a database connection.

    Returns:
        sqlite3.Connection: A connection to the database.
    """
    # Get the current working directory (root of the project when running from the command line)
    project_root = os.getcwd()

    # Construct the path to the database file
    db_path = os.path.join(project_root, 'disaster_alerts.db')

    # Connect to the database using the absolute path
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Optional: This allows column access by name (e.g., row['id'])

    return conn
