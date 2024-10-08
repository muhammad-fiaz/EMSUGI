from logly import logly
import os
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
from dotenv import load_dotenv
import pandas as pd
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer

# Load NLTK resources
nltk.download('punkt_tab')
nltk.download('stopwords')


# Load environment variables from .env file
load_dotenv()

# Get the Gemini API key from the environment variable
gemini_api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=gemini_api_key)

# CSV file for storing news articles
CSV_FILE = "disaster_alerts.csv"

# Predefined emergency words for generating keywords
EMERGENCY_WORDS = ['disaster', 'emergency', 'crisis', 'alert', 'warning', 'evacuation', 'flood', 'earthquake', 'fire',
                   'tornado', 'war', 'attack', 'explosion', 'pandemic', 'outbreak', 'epidemic', 'pandemic', 'virus', 'disease', 'infection', 'quarantine', 'lockdown', 'curfew', 'storm', 'volcano']

# Step 1: Function to Fetch Disaster and Emergency Alerts Using Bing News Search


def search_bing_for_alerts(query, num_results=5):
    logly.info(f"Starting search for '{query}' in Bing News...")
    search_url = f"https://www.bing.com/news/search?q={query}&FORM=HDRSC7"
    headers = {'User-Agent': 'Mozilla/5.0'}

    try:
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()  # Raises an error for 4xx/5xx responses

        logly.info("Search successful. Processing results...")
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []

        for li in soup.find_all('a', class_='title')[:num_results]:
            title = li.get_text() if li else "No title"
            link = li['href'] if li else "No link"
            country = "Israel"  # Extract country name if available
            content, tags = fetch_article_content_and_tags(link)
            keywords = generate_keywords(title, content)
            summary = generate_summary(content)

            results.append({
                'title': title,
                'link': link,
                'country': country,
                'summary': summary,
                'keywords': keywords,
                'tags': tags
            })

        logly.info(f"Found {len(results)} results.")
        return results

    except requests.exceptions.RequestException as e:
        logly.error(f"Failed to fetch search results: {e}")
        return []


# Function to fetch article content and generate tags
def fetch_article_content_and_tags(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract main content (this may vary based on the site's structure)
        paragraphs = soup.find_all('p')
        content = ' '.join([para.get_text()
                           for para in paragraphs if para.get_text()])

        # Generate tags from content
        tags = generate_tags(content)

        return content, tags
    except Exception as e:
        logly.error(f"Failed to fetch content from {url}: {e}")
        return "", []


# Function to generate a summary of the article
def generate_summary(content):
    sentences = nltk.sent_tokenize(content)
    if sentences:
        # Return the first two sentences as summary
        return ' '.join(sentences[:2])
    return ""


# Function to generate keywords based on title and content
def generate_keywords(title, content):
    combined_text = title + ' ' + content
    keywords = []

    # Include emergency words if they are found in the title or content
    for word in EMERGENCY_WORDS:
        if word in combined_text.lower():
            keywords.append(word)

    # Use TF-IDF to find additional keywords
    vectorizer = TfidfVectorizer(stop_words='english', max_features=5)
    tfidf_matrix = vectorizer.fit_transform([combined_text])
    feature_names = vectorizer.get_feature_names_out()

    # Combine predefined keywords with TF-IDF keywords
    keywords.extend([name for name in feature_names if name not in keywords])
    return list(set(keywords))  # Return unique keywords


# Function to generate tags from content
def generate_tags(content):
    words = nltk.word_tokenize(content)
    filtered_words = [word for word in words if
                      word.isalnum() and word.lower() not in nltk.corpus.stopwords.words('english')]
    return list(set(filtered_words))[:5]  # Return up to 5 unique tags


# Function to check if the URL already exists in the CSV
def is_url_existing(url):
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        return url in df['link'].values
    return False


# Function to append new articles to the CSV
def append_to_csv(alerts):
    new_alerts = []
    for alert in alerts:
        if not is_url_existing(alert['link']):
            new_alerts.append(alert)

    if new_alerts:
        df = pd.DataFrame(new_alerts)
        if os.path.exists(CSV_FILE):
            df.to_csv(CSV_FILE, mode='a', header=False, index=False)
        else:
            df.to_csv(CSV_FILE, index=False)


# Main function to execute the emergency management system
def main():
    location = "israel"
    query = location + " news today"
    num_results = 25  # Number of results to fetch

    # Search for emergency alerts using Bing News
    alerts = search_bing_for_alerts(query, num_results)

    # Append new articles to CSV if they don't already exist
    append_to_csv(alerts)

    # Generate a summary report using Gemini API
    if alerts:
        summary_report = generate_summary_report(alerts)
        print("Summary Report:\n")
        print(summary_report)
    else:
        print("No alerts found.")


# Function to generate a summary report using Gemini API
def generate_summary_report(alerts):
    report_text = "\n".join([
        f"{alert['title']}: {alert['link']}\nCountry: {alert['country']}\nSummary: {alert['summary']}\nKeywords: {', '.join(alert['keywords'])}\nTags: {', '.join(alert['tags'])}\n"
        for alert in alerts])
    prompt = f"Generate a news summary report and precaution for peoples for the following emergency alerts:\n\n{report_text}"
    model = genai.GenerativeModel(model_name='gemini-1.5-flash')

    response = model.generate_content(prompt)
    return response.text


if __name__ == "__main__":
    main()
