from flask import session, flash, redirect, url_for


def cancel_report_generation():
    """
    Allows the user to cancel the ongoing report generation process.
    """
    # Set the cancellation flag in the session
    session['cancel_generation'] = True
    flash("Generation process has been canceled.")
    return redirect(url_for('index'))  # Redirect to the main page or another appropriate page
