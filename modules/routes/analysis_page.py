from flask import request, render_template
from logly import logly


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
