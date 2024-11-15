# MIT License
#
# Copyright (c) 2024 Muhammad Fiaz
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import base64
import io
import os

import numpy as np
import requests
from bs4 import BeautifulSoup
import nltk
import sqlite3
import matplotlib.pyplot as plt
import pandas as pd
import markdown  # Import the markdown library
from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
from logly import logly

from fetch_alerts import fetch_and_store_alerts
from database import init_db
from datetime import datetime, timedelta

os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

from generate import  Generate

# Load NLTK resources
nltk.download('punkt')
nltk.download('stopwords')


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")  # Make sure to set this in your .env file
API_ENABLED = os.getenv("API_ENABLED", "False").lower() == "true"
DEBUG=os.getenv("DEBUG", "False").lower() == "true"

@app.route('/', methods=['GET'])
def index():
    """
    Renders the index page and clears the session variable.

    Returns:
        str: Rendered HTML template for the index page.
    """
    # Clear session variable on accessing the index page
    session.pop('can_access_report', None)
    return render_template('index.html')

@app.route('/reports', methods=['GET'])
def reports():
    """
      Retrieves all Gemini reports from the database and renders the reports page.

      Returns:
          str: Rendered HTML template for the reports page with fetched data.
      """
    # Connect to the database
    conn = sqlite3.connect('disaster_alerts.db')
    c = conn.cursor()

    # Retrieve all gemini reports from the database, including created_at
    c.execute("SELECT id, report, created_at FROM gemini_reports ORDER BY id DESC")
    gemini_reports = c.fetchall()

    conn.close()
    logly.info(f"Retrieved Gemini reports")
    # Render the reports template with the fetched data
    return render_template('reports.html', gemini_reports=gemini_reports)

@app.route('/loading', methods=['POST'])
def loading():
    """
     Fetches alerts for a given location and processes the data.

     Args:
         location (str): The location to search for news alerts.
         topic (str): The topic to search for news alerts.

     Returns:
         json: JSON object indicating that processing is complete.
     """
    location = request.form.get('location')
    topic = request.form.get('topic')
    logly.info(f"Received location: {location}")
    logly.info(f"Received topic: {topic}")
    # Fetch alerts and process data
    fetch_and_store_alerts(location,topic, num_results=25)

    # Set session variable to allow access to the report page
    session['can_access_report'] = True
    logly.info("fetching alerts and processing data")
    # Respond with a JSON object indicating that processing is complete
    return jsonify({'status': 'completed'})

@app.route('/analysis-data', methods=['GET'])
def fetch_analysis_data():
    """
    Fetches distinct values for locations, tags, priorities, and keywords from the database,
    along with future prediction durations and additional timeframes for past data.

    Returns:
        json: A dictionary with lists of locations, tags, priorities, keywords, prediction durations, and past date ranges.
    """
    # Connect to the database
    conn = sqlite3.connect('disaster_alerts.db')
    c = conn.cursor()

    # Fetch distinct locations
    c.execute("SELECT DISTINCT country FROM alerts")
    locations = [row[0] for row in c.fetchall()]

    # Fetch and process distinct tags
    c.execute("SELECT DISTINCT tags FROM alerts")
    raw_tags = [row[0] for row in c.fetchall()]
    distinct_tags = set()
    for tag_list in raw_tags:
        if tag_list:
            distinct_tags.update([tag.strip() for tag in tag_list.split(',') if not tag.strip().isdigit()])

    # Fetch and process distinct keywords
    c.execute("SELECT DISTINCT keywords FROM alerts")
    raw_keywords = [row[0] for row in c.fetchall()]
    distinct_keywords = set()
    for keyword_list in raw_keywords:
        if keyword_list:
            distinct_keywords.update(
                [keyword.strip() for keyword in keyword_list.split(',') if not keyword.strip().isdigit()])
    # Fetch distinct priorities
    c.execute("SELECT DISTINCT priority FROM alerts")
    priorities = [row[0] for row in c.fetchall()]

    conn.close()

    # Define prediction durations (future intervals)
    prediction_durations = {
        "durations": [
            {"label": "1 Week", "value": 7},  # 7 days
            {"label": "2 Weeks", "value": 14},  # 14 days
            {"label": "1 Month", "value": 30},  # 30 days
            {"label": "3 Months", "value": 90}  # 90 days
        ]
    }

    # Define past date ranges
    past_date_ranges = [
        {"label": "Last Year to This Month", "value": "last_year_to_this_month"},
        {"label": "Last Week", "value": "last_week"},
        {"label": "Last 7 Days", "value": "last_7_days"}
    ]

    # Return data as JSON
    return jsonify({
        'locations': locations,
        'tags': sorted(distinct_tags),
        'priorities': priorities,
        'keywords': sorted(distinct_keywords),
        'prediction_durations': prediction_durations,
        'past_date_ranges': past_date_ranges
    })



@app.route('/records', methods=['GET'])
def history():
    """
      Retrieves all historical alert data from the database and renders the records page.

      Returns:
          str: Rendered HTML template for the records page with fetched data.
      """
    # Connect to the database
    conn = sqlite3.connect('disaster_alerts.db')
    c = conn.cursor()

    # Retrieve all records data in descending order (most recent first)
    c.execute("SELECT * FROM alerts ORDER BY id DESC")
    records_data = c.fetchall()

    conn.close()
    logly.info(f"Retrieved records data")
    # Render the records template with the fetched data
    return render_template('records.html', records=records_data)


@app.route('/report', methods=['GET'])
def report():
    # Check access permissions
    if not session.get('can_access_report'):
        flash("You need to perform a search first.")
        return redirect(url_for('index'))

    # Retrieve data from the database
    conn = sqlite3.connect('disaster_alerts.db')
    c = conn.cursor()
    # First query: Get data ordered by 'id' DESC
    c.execute("SELECT * FROM current_alerts ORDER BY id DESC")
    current_alerts= c.fetchall()

    # Second query: Get data ordered by 'keywords' ASC
    c.execute("SELECT keywords FROM current_alerts ORDER BY keywords ASC")
    current_alerts_by_keywords = c.fetchall()
    conn.close()

    # Generate analysis data for charts
    chart_data = generate_analysis_charts(current_alerts_by_keywords)
    logly.warn(f"Generated analysis data for charts"+str(chart_data))
    gemini_report = generate_gemini_report(current_alerts)

    # Clear session variable after rendering the report
    session.pop('can_access_report', None)
    return render_template('report.html', alerts=current_alerts, chart_data=chart_data, gemini_report=gemini_report)


@app.route('/regenerate-report', methods=['POST'])
def regenerate_report():
    """
    Regenerates a report based on current alerts and returns it as JSON.

    Returns:
        json: JSON object containing the regenerated report.
    """
    # Retrieve data from the current_alerts table
    conn = sqlite3.connect('disaster_alerts.db')
    c = conn.cursor()
    c.execute("SELECT * FROM current_alerts ORDER BY id DESC")
    current_alerts = c.fetchall()
    conn.close()

    # Generate a new report using the current alerts
    gemini_report = generate_gemini_report(current_alerts)

    # Return the new report as JSON
    logly.info(f"Regenerated report")
    return jsonify({'report': gemini_report})


def generate_analysis_charts(alerts_by_keywords):
    """
    Generates analysis data based on the provided alerts ordered by keywords for rendering charts on the front end.

    Args:
        alerts_by_keywords (list): A list of tuples containing alert details ordered by 'keywords'.

    Returns:
        dict: JSON-compatible dictionary with keyword frequencies.
    """
    # Dictionary to store keyword frequencies for alerts ordered by keywords
    keyword_counts_by_keywords = {}

    logly.warn(f"Generating analysis data for charts for alerts ordered by keywords...")

    # Loop through each alert to split and count keywords
    for alert in alerts_by_keywords:
        logly.warn(f"Generating analysis data for alerts ordered by keywords..."+str(alert))
        # Splitting by ',' and removing leading/trailing spaces for each keyword
        keywords = [keyword.strip() for keyword in alert[0].split(',')]
        logly.warn(f"Generating analysis data for alerts ordered by keywords..."+str(keywords))
        # Count the frequency of each keyword
        for keyword in keywords:
            # ignore numbers only without any words in keywords
            if keyword and not keyword.isdigit():
                keyword_counts_by_keywords[keyword] = keyword_counts_by_keywords.get(keyword, 0) + 1

    # Log the generated keyword counts for verification
    logly.warn(f"Generated keyword counts for alerts ordered by keywords: {keyword_counts_by_keywords}")

    # Return the keyword frequency data for alerts ordered by keywords
    return keyword_counts_by_keywords




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

    report_sentences = Generate(report_data, api=API_ENABLED).generate_report()
    # Convert the Markdown response to HTML
    report_html = markdown.markdown(report_sentences)

    # Store the generated report in the database with the current timestamp
    conn = sqlite3.connect('disaster_alerts.db')
    c = conn.cursor()
    c.execute("INSERT INTO gemini_reports (report, created_at) VALUES (?, ?)", (report_html, datetime.now()))
    conn.commit()
    conn.close()
    logly.info(f"Generated Gemini report")
    return report_html


# Route to render the analysis page (GET request)
@app.route('/analysis', methods=['GET', 'POST'])
def analysis():
    if request.method == 'POST':
        # Here we will handle the form submission (e.g., generating analysis chart)
        location = request.form.get('location')
        keywords = request.form.getlist('keywords')  # get multiple selected values
        tags = request.form.getlist('tags')

        # You can process the form data here and return a response if needed
        # Example: Store filters in session or handle backend processing for predictions
        # For now, we'll just send back an empty response for demonstration
        logly.info(f"Received form data: {location}, {keywords}, {tags}")
        return render_template('analysis.html', location=location, keywords=keywords, tags=tags)

    logly.info("Rendering analysis page")
    # Default GET request renders the form page
    return render_template('analysis.html')



@app.route('/license', methods=['GET'])
def license():
    """
    Renders the License page.

    Returns:
        str: Rendered HTML template for the License page.
    """
    return render_template('license.html')

@app.route('/notice', methods=['GET'])
def notice():
    """
    Renders the Notice page.

    Returns:
        str: Rendered HTML template for the Notice page.
    """
    return render_template('notice.html')
