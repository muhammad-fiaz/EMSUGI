"""
This script initializes the database and starts the Flask application server.
It should be run directly as the main program.

The script does the following:
1. Imports necessary modules and functions.
2. Initializes the database.
3. Runs the Flask application with debug mode set according to the DEBUG constant.

Imports:
    app (Flask): The Flask application instance.
    DEBUG (bool): A boolean flag to enable/disable debug mode.
    init_db (function): A function to initialize the database.

Usage:
    python launch.py
"""
from app import app, DEBUG
from database import init_db

if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(debug=DEBUG)
