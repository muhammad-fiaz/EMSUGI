import datetime
import random

from flask import jsonify, request

from modules.db import get_db_connection


def fetch_analysis_data() -> dict:
    """
    Fetches distinct values for locations, tags, priorities, and keywords from the database,
    along with future prediction durations and additional timeframes for past data.

    Returns:
        json: A dictionary with lists of locations, tags, priorities, keywords, prediction durations, and past date ranges.
    """
    # Connect to the database
    conn = get_db_connection()
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




def get_predictions()-> dict:
    """
    Generate simulated prediction data based on selected filters such as location, tags, etc.
    """
    # Extract query parameters for filters
    location = request.args.get('location', 'overall')
    keywords = request.args.get('keywords', 'overall')
    tags = request.args.get('tags', 'overall')
    duration = int(request.args.get('duration', '30'))  # Default to 30 days

    # Generate simulated prediction data (replace this with actual model logic)
    timeline_dates = generate_dates(duration)
    timeline_predictions = generate_predictions(len(timeline_dates))
    histogram_data = [random.randint(10, 50) for _ in range(5)]
    bar_data = [random.randint(50, 100) for _ in range(4)]
    pie_data = [random.randint(20, 40) for _ in range(3)]

    return jsonify({
        'timeline': {
            'dates': timeline_dates,
            'predictions': timeline_predictions,
        },
        'histogram': histogram_data,
        'bar_chart': bar_data,
        'pie_chart': pie_data
    })


def generate_dates(duration):
    """Generate dates for the timeline based on duration."""
    start_date = datetime.datetime.now()
    return [(start_date + datetime.timedelta(days=30 * i)).strftime('%Y-%m-%d') for i in range(duration)]


def generate_predictions(n):
    """Generate random prediction values."""
    return [random.randint(50, 100) for _ in range(n)]



