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

import os
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
from dotenv import load_dotenv
import nltk
import sqlite3
import matplotlib.pyplot as plt
import pandas as pd
import markdown  # Import the markdown library
from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
from fetch_alerts import fetch_and_store_alerts
from database import init_db
from datetime import datetime

# Load NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

# Load environment variables from .env file
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=gemini_api_key)

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")  # Make sure to set this in your .env file


@app.route('/', methods=['GET'])
def index():
    # Clear session variable on accessing the index page
    session.pop('can_access_report', None)
    return render_template('index.html')

@app.route('/reports', methods=['GET'])
def reports():
    # Connect to the database
    conn = sqlite3.connect('disaster_alerts.db')
    c = conn.cursor()

    # Retrieve all gemini reports from the database, including created_at
    c.execute("SELECT id, report, created_at FROM gemini_reports ORDER BY id DESC")
    gemini_reports = c.fetchall()

    conn.close()

    # Render the reports template with the fetched data
    return render_template('reports.html', gemini_reports=gemini_reports)

@app.route('/loading', methods=['POST'])
def loading():
    location = request.form['location']

    # Fetch alerts and process data
    fetch_and_store_alerts(location, num_results=25)

    # Set session variable to allow access to the report page
    session['can_access_report'] = True

    # Respond with a JSON object indicating that processing is complete
    return jsonify({'status': 'completed'})


@app.route('/history', methods=['GET'])
def history():
    # Connect to the database
    conn = sqlite3.connect('disaster_alerts.db')
    c = conn.cursor()

    # Retrieve all history data in descending order (most recent first)
    c.execute("SELECT * FROM alerts ORDER BY id DESC")
    history_data = c.fetchall()

    conn.close()

    # Render the history template with the fetched data
    return render_template('history.html', history=history_data)


@app.route('/report', methods=['GET'])
def report():
    # Check if the user is allowed to access this page
    if not session.get('can_access_report'):
        flash("You need to perform a search first.")
        return redirect(url_for('index'))  # Redirect to the main page if not allowed

    # Retrieve data from the current_alerts table
    conn = sqlite3.connect('disaster_alerts.db')
    c = conn.cursor()
    c.execute("SELECT * FROM current_alerts ORDER BY id DESC")
    current_alerts = c.fetchall()
    conn.close()

    # Generate charts and report based on current alerts
    charts = generate_analysis_charts(current_alerts)
    if not charts:
        return "No data available to generate charts."

    gemini_report = generate_gemini_report(current_alerts)

    # Clear the session variable after rendering the report
    session.pop('can_access_report', None)

    # Render the report page
    return render_template('report.html', alerts=current_alerts, charts=charts, gemini_report=gemini_report)


@app.route('/regenerate-report', methods=['POST'])
def regenerate_report():
    # Retrieve data from the current_alerts table
    conn = sqlite3.connect('disaster_alerts.db')
    c = conn.cursor()
    c.execute("SELECT * FROM current_alerts ORDER BY id DESC")
    current_alerts = c.fetchall()
    conn.close()

    # Generate a new report using the current alerts
    gemini_report = generate_gemini_report(current_alerts)

    # Return the new report as JSON
    return jsonify({'report': gemini_report})



def generate_analysis_charts(alerts):
    charts = []

    # Create DataFrame for analysis
    keywords_list = []
    dates_list = []
    countries_list = []

    for alert in alerts:
        # Split the keywords (assuming they are comma-separated)
        keywords = alert[4].split(', ')  # Assuming keywords are in the 5th column
        # Append each keyword to the keywords_list
        keywords_list.extend(keywords)
        # Append the current date to the dates_list for each keyword
        for keyword in keywords:
            dates_list.append(datetime.now())  # Use current datetime for demo purposes
            countries_list.append(alert[3])  # Assuming country is in the 3rd column

    # Ensure the lengths of lists are consistent before creating the DataFrame
    if len(keywords_list) != len(dates_list) or len(keywords_list) != len(countries_list):
        raise ValueError("The lengths of keywords, dates, and countries lists are not the same.")

    df = pd.DataFrame({
        'keywords': keywords_list,
        'dates': dates_list,
        'countries': countries_list
    })

    # Generate Keyword Frequency Histogram
    keyword_counts = df['keywords'].value_counts()
    plt.figure(figsize=(10, 6))
    keyword_counts.plot(kind='bar', color='blue')
    plt.title('Keyword Frequency Analysis')
    plt.xlabel('Keywords')
    plt.ylabel('Frequency')
    histogram_file = 'static/keyword_frequency.png'
    plt.savefig(histogram_file)
    plt.close()
    charts.append(histogram_file)

    return charts


def generate_gemini_report(alerts):
    # Create a report based on alerts
    report_data = []
    for alert in alerts:
        report_data.append({
            'title': alert[1],  # Assuming title is in the 2nd column
            'summary': alert[4],  # Assuming summary is in the 5th column
            'link': alert[2],  # Assuming link is in the 3rd column
        })

    # Generate report text using Gemini AI
    report_text = genai.GenerativeModel(model_name='gemini-1.5-flash')
    report_text = report_text.generate_content(
        f"you are now a Reporter you will help people to report the emergency time about current scenario, so Generate an emergency and disaster and war times summary report and precaution for people for the following emergency alerts:\n\n{report_data}")


    # Convert the Markdown response to HTML
    report_html = markdown.markdown(report_text.text)

    # Store the generated report in the database with the current timestamp
    conn = sqlite3.connect('disaster_alerts.db')
    c = conn.cursor()
    c.execute("INSERT INTO gemini_reports (report, created_at) VALUES (?, ?)", (report_html, datetime.now()))
    conn.commit()
    conn.close()

    return report_html




if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(debug=True)
