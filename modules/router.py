import os
from flask import Flask

from modules.routes import index, reports, analysis, records, license_router, notice, report
from modules.api import fetch_analysis_data, regenerate_report, loading_api, cancel_report_generation


def create_app():
    app = Flask(__name__, template_folder=os.path.abspath('templates'), static_folder=os.path.abspath('static'))
    app.secret_key = os.getenv("SECRET_KEY")  # Ensure .env contains this key

    # Register routes
    app.add_url_rule('/', 'index', index)
    app.add_url_rule('/reports', 'reports', reports)
    app.add_url_rule('/analysis', 'analysis', analysis, methods=['GET', 'POST'])
    app.add_url_rule('/report', 'report', report)
    app.add_url_rule('/license', 'license', license_router)
    app.add_url_rule('/notice', 'notice', notice)
    app.add_url_rule('/records', 'records', records, methods=['GET', 'POST'])

    # Register API routes
    app.add_url_rule('/api/loading', 'loading', loading_api, methods=['GET', 'POST'])
    app.add_url_rule('/api/analysis-data', 'analysis-data', fetch_analysis_data, methods=['GET'])
    app.add_url_rule('/api/regenerate-report', 'regenerate-report', regenerate_report, methods=['POST'])
    app.add_url_rule('/cancel_report_generation', 'cancel_report_generation', cancel_report_generation,
                     methods=['POST'])

    return app