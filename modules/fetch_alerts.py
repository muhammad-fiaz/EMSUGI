import os
import sqlite3


import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
from dotenv import load_dotenv
from flask import session
from logly import logly

from modules.db import get_db_connection
from modules.process import fetch_article_content_and_tags, generate_summary, generate_keywords, \
    determine_priority
from modules.utils.check_for_cancel import check_for_cancel

# Get the Gemini API key from the environment variable
gemini_api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=gemini_api_key)

# Predefined emergency words for generating keywords
EMERGENCY_WORDS = ["earthquake", "flood", "storm", "fire", "evacuation"]
from datetime import datetime  # Import datetime



def fetch_and_store_alerts(location,topic, num_results=5):
    """
    Fetches news alerts for a given location and stores them in the database.

    Args:
        topic (str): The topic to search for news alerts.
        location (str): The location to search for news alerts.
        num_results (int): The number of results to fetch. Defaults to 5.

    Returns:
        list: A list of tuples containing the fetched alert details.
    """
    query = f"{topic} on {location} news today"
    logly.info(f"Starting search for '{query}' in Bing News...")
    search_url = f"https://www.bing.com/news/search?q={query}&FORM=HDRSC7"
    headers = {'User-Agent': 'Mozilla/5.0'}

    results = []  # Store fetched results to return

    try:
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        for li in soup.find_all('a', class_='title')[:num_results]:
            # Check if cancellation has been requested before making the API call
            if check_for_cancel():
                logly.info("Report generation was canceled by the user.")
                return "Process canceled by user."

            title = li.get_text() if li else "No title"
            link = li['href'] if li else "No link"
            country = location  # Use the user-provided location as the country
            content, tags = fetch_article_content_and_tags(link)
            keywords = generate_keywords(title, content)
            summary = generate_summary(content)
            priority = determine_priority(summary)
            logly.info('details for the alert done!')
            # Get the current date
            date =  datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logly.info(f"Date: {date}")
            results.append((title, link, country, summary, ', '.join(keywords), ', '.join(tags), date, priority))
        logly.info(f"Found {len(results)} results.")
        # Store results in SQLite
        store_results_in_current_db(results)
        store_results_in_db(results)  # Store priority too

    except requests.exceptions.RequestException as e:
        logly.error(f"Failed to fetch search results: {e}")

    return results  # Return fetched results


def store_results_in_current_db(alerts):
    """
     Stores the fetched alerts in the current_alerts table in the database.

     Args:
         alerts (list): A list of tuples containing the alert details.
     """
    conn = get_db_connection()
    c = conn.cursor()

    # Check if the current_alerts table is empty
    c.execute("SELECT COUNT(*) FROM current_alerts")
    count = c.fetchone()[0]

    # Clear the current_alerts table only if it's not empty
    if count > 0:
        c.execute("DELETE FROM current_alerts")

    # Append new alerts to the current_alerts table
    for alert in alerts:
        try:
            logly.info(f"Storing alert in current alerts table: {alert}")
            c.execute('''INSERT INTO current_alerts (title, link, country, summary, keywords, tags, date, priority)
                          VALUES (?, ?, ?, ?, ?, ?, ?,?)''', alert)
        except Exception as e:
            logly.error(f"Error inserting alert into current alerts table: {e}")

    conn.commit()
    conn.close()


def store_results_in_db(alerts):
    """
    Stores the fetched alerts in the alerts records table in the database.

    Args:
        alerts (list): A list of tuples containing the alert details.
    """
    conn = get_db_connection()
    c = conn.cursor()

    # Append new alerts to the existing records without deleting
    for alert in alerts:
        title, link, country, summary, keywords, tags, date,priority = alert


        try:
            # Check if cancellation has been requested before making the API call
            if check_for_cancel():
                logly.info("Report generation was canceled by the user.")
                return "Process canceled by user."
            logly.info(f"Storing alert in alerts table: {alert}")
            c.execute('''INSERT OR IGNORE INTO alerts (title, link, country, summary, keywords, tags, date, priority)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                      (title, link, country, summary, keywords, tags, date, priority))

        except Exception as e:
            logly.error(f"Error inserting alert into database: {e}")

    conn.commit()
    conn.close()

