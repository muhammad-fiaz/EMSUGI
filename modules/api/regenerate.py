import sqlite3

from flask import jsonify
from logly import logly

from modules.db import get_db_connection
from modules.utils.generate_gemini_report import generate_gemini_report


def regenerate_report()-> dict:
    """
    Regenerates a report based on current alerts and returns it as JSON.

    Returns:
        json: JSON object containing the regenerated report.
    """
    # Retrieve data from the current_alerts table
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM current_alerts ORDER BY id DESC")
    current_alerts = c.fetchall()
    conn.close()

    # Generate a new report using the current alerts
    gemini_report = generate_gemini_report(current_alerts)

    # Return the new report as JSON
    logly.info(f"Regenerated report")
    return jsonify({'report': gemini_report})

