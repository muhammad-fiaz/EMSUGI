import os
import sqlite3
from datetime import datetime
import markdown
from logly import logly
from modules.db import get_db_connection
from modules.generate import Generate
from modules.utils.check_for_cancel import check_for_cancel

API_ENABLED = os.getenv("API_ENABLED", "False").lower() == "true"

def generate_gemini_report(alerts):
    """
    Generates a report based on the provided alerts using Gemini AI.

    Args:
        alerts (list): A list of tuples containing alert details.

    Returns:
        str: The generated report in HTML format.
    """
    # Create a report based on alerts
    report_data = []
    for alert in alerts:
        report_data.append({
            'title': alert[1],  # Assuming title is in the 2nd column
            'summary': alert[4],  # Assuming summary is in the 5th column
            'link': alert[2],  # Assuming link is in the 3rd column
        })

    # Create an instance of Generate and generate the report
    report_generator = Generate(report_data, api=API_ENABLED)

    # Check for cancellation before starting the generation process
    if check_for_cancel():
        logly.info("Report generation was canceled before starting.")
        return "Report generation canceled."

    report_sentences = report_generator.generate_report()

    # Convert the Markdown response to HTML
    report_html = markdown.markdown(report_sentences)

    # Store the generated report in the database with the current timestamp
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("INSERT INTO gemini_reports (report, created_at) VALUES (?, ?)", (report_html, datetime.now()))
    conn.commit()
    conn.close()
    logly.info(f"Generated Gemini report")
    return report_html
