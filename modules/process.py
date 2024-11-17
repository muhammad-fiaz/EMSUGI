import requests
from bs4 import BeautifulSoup
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
import time
import random
from logly import logly

from modules.utils.check_for_cancel import check_for_cancel

# Predefined emergency words for generating keywords
EMERGENCY_WORDS = ['disaster', 'emergency', 'crisis', 'alert', 'warning', 'evacuation', 'flood', 'earthquake', 'fire',
                   'tornado', 'war', 'attack', 'explosion', 'pandemic', 'outbreak', 'epidemic', 'pandemic', 'virus',
                   'disease', 'infection', 'quarantine'
    , 'lockdown', 'curfew', 'storm', 'volcano']


# Function to fetch random user-agent (for anti-scraping purposes)
def get_random_user_agent():
    """
      This function selects a random user-agent from a predefined list to be used in HTTP requests.
      This is done to evade detection by websites that block or limit access based on user-agent strings.

      Returns:
          str: A randomly selected user-agent string.
      """
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.113 Safari/537.36'
    ]
    return random.choice(user_agents)


# Function to fetch article content and generate tags with recursive retries
def fetch_article_content_and_tags(url, retries=3):
    """
       Fetches the content of an article and generates tags with automatic retries on failure.

       Args:
           url (str): The URL of the article.
           retries (int): The number of retries if the request fails. Defaults to 3.

       Returns:
           tuple: A tuple containing the article content and a list of tags.
    """
    try:
        # Check if cancellation has been requested before making the API call
        if check_for_cancel():
            logly.info("Report generation was canceled by the user.")
            return "Process canceled by user."
        response = requests.get(url, headers={'User-Agent': get_random_user_agent()})
        response.raise_for_status()  # Will raise an error for 4xx/5xx responses

        # Parse the article content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract main content (this may vary based on the site's structure)
        paragraphs = soup.find_all('p')
        content = ' '.join([para.get_text() for para in paragraphs if para.get_text()])

        # Generate tags from content
        tags = generate_tags(content)
        logly.info(f"Tags generated: {tags}")
        return content, tags

    except requests.exceptions.RequestException as e:
        logly.error(f"Failed to fetch content from {url}. Error: {e}")

        # Check if retries are available
        if retries > 0:
            logly.info(f"Retrying... {retries} attempts left.")
            time.sleep(random.uniform(1, 3))  # Small delay before retry
            return fetch_article_content_and_tags(url, retries - 1)  # Recursive retry
        else:
            logly.error(f"Max retries reached. Skipping {url}.")
            return "", []  # Return empty content and tags if retries are exhausted


# Function to determine the priority of the alert based on the summary
def determine_priority(summary):
    """
    Determines the priority level based on the summary of the alert.

    Args:
        summary (str): The summary of the alert.

    Returns:
        str: The priority level ('high', 'medium', 'low').
    """
    high_priority_keywords = ['emergency', 'crisis', 'evacuation', 'warning', 'attack', 'disaster', 'explosion', 'war',
                              'fire', 'terrorist', 'danger']
    medium_priority_keywords = ['flood', 'storm', 'earthquake', 'tornado', 'volcano', 'pandemic', 'outbreak',
                                'epidemic', 'virus', 'disease', 'infection', 'quarantine', 'lockdown', 'curfew']
    low_priority_keywords = ['report', 'survey', 'update', 'analysis']

    summary_lower = summary.lower()

    # Check for high priority
    if any(keyword in summary_lower for keyword in high_priority_keywords):
        logly.info("Priority: High")
        return 'high'
    # Check for medium priority
    elif any(keyword in summary_lower for keyword in medium_priority_keywords):
        logly.info("Priority: Medium")
        return 'medium'
    # Check for low priority
    elif any(keyword in summary_lower for keyword in low_priority_keywords):
        logly.info("Priority: Low")
        return 'low'
    logly.info("Priority: Low")
    return 'low'  # Default to low if no match found


# Function to generate a summary of the article
def generate_summary(content):
    """
      Generates a summary of the article content.

      Args:
          content (str): The content of the article.

      Returns:
          str: A summary of the article.
    """
    sentences = nltk.sent_tokenize(content)
    if sentences:
        logly.info(f"Summary: {sentences[:2]}")
        return ' '.join(sentences[:2])  # Return the first two sentences as summary
    logly.info("Summary: No content")
    return "Summary not available"


# Function to generate keywords based on title and content
def generate_keywords(title, content):
    """
        Generates keywords based on the title and content of the article.

        Args:
            title (str): The title of the article.
            content (str): The content of the article.

        Returns:
            list: A list of keywords.
    """
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
    logly.info(f"Keywords generated: {keywords}")
    return list(set(keywords))  # Return unique keywords


# Function to generate tags from content
def generate_tags(content):
    """
      Generates tags from the article content.

      Args:
          content (str): The content of the article.

      Returns:
          list: A list of tags.
    """
    words = nltk.word_tokenize(content)
    filtered_words = [word for word in words if
                      word.isalnum() and word.lower() not in nltk.corpus.stopwords.words('english')]
    logly.info(f"Tags generated: {filtered_words[:5]}")
    return list(set(filtered_words))[:5]  # Return up to 5 unique tags
