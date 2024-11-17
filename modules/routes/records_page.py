from flask import render_template
from logly import logly

from modules.db import get_db_connection


def records():
    """
      Retrieves all historical alert data from the database and renders the records page.

      Returns:
          str: Rendered HTML template for the records page with fetched data.
      """
    # Connect to the database
    conn = get_db_connection()

    c = conn.cursor()

    # Retrieve all records data in descending order (most recent first)
    c.execute("SELECT * FROM alerts ORDER BY id DESC")
    records_data = c.fetchall()

    conn.close()
    logly.info(f"Retrieved records data")
    # Render the records template with the fetched data
    return render_template('records.html', records=records_data)

