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
from flask import Flask, render_template, request, redirect, url_for
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

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        location = request.form['location']  # Get the user input

        fetch_and_store_alerts(location, num_results=25)  # Fetch alerts based on user input
        return redirect(url_for('index'))  # Redirect to GET method to display alerts

    # For GET request, retrieve data from the database
    conn = sqlite3.connect('disaster_alerts.db')
    c = conn.cursor()
    c.execute("SELECT * FROM alerts ORDER BY id DESC")  # Fetch alerts in reverse order
    alerts = c.fetchall()
    conn.close()

    # Generate analysis charts
    charts = generate_analysis_charts(alerts)

    # Generate Gemini report
    gemini_report = generate_gemini_report(alerts)

    return render_template('index.html', alerts=alerts, charts=charts, gemini_report=gemini_report)

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
        f"you are now a Reporter you will help people to report the emergency time about current scenerio, so Generate a emergency and disaster and war times summary report and precaution for people for the following emergency alerts:\n\n{report_data}")

    # Convert the Markdown response to HTML
    report_html = markdown.markdown(report_text.text)

    return report_html

if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(debug=True)