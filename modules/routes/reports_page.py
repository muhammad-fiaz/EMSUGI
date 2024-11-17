import os
import sqlite3

from flask import render_template
from logly import logly

from modules.db import get_db_connection


def reports():
    """
      Retrieves all Gemini reports from the database and renders the reports page.

      Returns:
          str: Rendered HTML template for the reports page with fetched data.
      """
    # Get the root path of the project
    conn = get_db_connection()
    c = conn.cursor()

    # Retrieve all gemini reports from the database, including created_at
    c.execute("SELECT id, report, created_at FROM gemini_reports ORDER BY id DESC")
    gemini_reports = c.fetchall()

    conn.close()
    logly.info(f"Retrieved Gemini reports")
    # Render the reports template with the fetched data
    return render_template('reports.html', gemini_reports=gemini_reports)
