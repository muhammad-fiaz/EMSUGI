import sqlite3
from flask import session, redirect, flash, url_for, render_template
from logly import logly

from modules.db import get_db_connection
from modules.utils.generate_analysis_charts import generate_analysis_charts
from modules.utils.generate_gemini_report import generate_gemini_report


def report():
    # Check access permissions
    if not session.get('can_access_report'):
        flash("You need to perform a search first.")
        return redirect(url_for('index'))

    # Retrieve data from the database
    conn = get_db_connection()
    c = conn.cursor()
    # First query: Get data ordered by 'id' DESC
    c.execute("SELECT * FROM current_alerts ORDER BY id DESC")
    current_alerts = c.fetchall()

    # Second query: Get data ordered by 'keywords' ASC
    c.execute("SELECT keywords FROM current_alerts ORDER BY keywords ASC")
    current_alerts_by_keywords = c.fetchall()
    conn.close()

    # Generate analysis data for charts
    chart_data = generate_analysis_charts(current_alerts_by_keywords)
    logly.warn(f"Generated analysis data for charts" + str(chart_data))

    # Generate report using Gemini AI
    gemini_report = generate_gemini_report(current_alerts)

    # Clear session variable after rendering the report
    session.pop('can_access_report', None)
    return render_template('report.html', alerts=current_alerts, chart_data=chart_data, gemini_report=gemini_report)
