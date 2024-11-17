from flask import session, render_template


def index():
    """
    Renders the index page and clears the session variable.

    Returns:
        str: Rendered HTML template for the index page.
    """
    # Clear session variable on accessing the index page
    session.pop('can_access_report', None)
    return render_template('index.html')
