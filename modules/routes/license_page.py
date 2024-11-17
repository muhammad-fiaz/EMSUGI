from flask import render_template


def license_router():
    """
    Renders the License page.

    Returns:
        str: Rendered HTML template for the License page.
    """
    return render_template('license.html')

