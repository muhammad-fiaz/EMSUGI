from flask import session


def check_for_cancel():
    """Check if the report generation has been canceled."""
    return session.get('cancel_generation', False)

