from flask import request, session, jsonify
from logly import logly

from modules.fetch_alerts import fetch_and_store_alerts


def loading_api() -> dict:
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
