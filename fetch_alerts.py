import os
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
from dotenv import load_dotenv
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
import sqlite3
from logly import logly

from backend.report_general import generate_keywords, fetch_article_content_and_tags, generate_summary

# Load NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

# Load environment variables from .env file
load_dotenv()

# Get the Gemini API key from the environment variable
gemini_api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=gemini_api_key)

# Predefined emergency words for generating keywords
EMERGENCY_WORDS = [...]  # Your emergency words list here


# Function to fetch and store alerts
def fetch_and_store_alerts(location, num_results=5):
    query = f"{location} news today"
    logly.info(f"Starting search for '{query}' in Bing News...")
    search_url = f"https://www.bing.com/news/search?q={query}&FORM=HDRSC7"
    headers = {'User-Agent': 'Mozilla/5.0'}

    try:
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []

        for li in soup.find_all('a', class_='title')[:num_results]:
            title = li.get_text() if li else "No title"
            link = li['href'] if li else "No link"
            country = location  # Use the user-provided location as the country
            content, tags = fetch_article_content_and_tags(link)
            keywords = generate_keywords(title, content)
            summary = generate_summary(content)

            results.append((title, link, country, summary, ', '.join(keywords), ', '.join(tags)))

        # Store results in SQLite, first clear previous alerts
        store_results_in_db(results)

    except requests.exceptions.RequestException as e:
        logly.error(f"Failed to fetch search results: {e}")


def store_results_in_db(alerts):
    conn = sqlite3.connect('disaster_alerts.db')
    c = conn.cursor()

    # Clear existing alerts for the given location
    c.execute("DELETE FROM alerts")  # This will remove previous alerts

    for alert in alerts:
        try:
            c.execute('''INSERT INTO alerts (title, link, country, summary, keywords, tags)
                          VALUES (?, ?, ?, ?, ?, ?)''', alert)
        except Exception as e:
            logly.error(f"Error inserting alert into database: {e}")

    conn.commit()
    conn.close()
