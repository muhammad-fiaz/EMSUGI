from logly import logly


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
