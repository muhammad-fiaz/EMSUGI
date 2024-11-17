from flask import render_template


def notice():
    """
    Renders the Notice page.

    Returns:
        str: Rendered HTML template for the Notice page.
    """
    return render_template('notice.html')