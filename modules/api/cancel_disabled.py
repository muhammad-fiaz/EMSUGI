from flask import jsonify

def cancel_disabled():
    # Logic to stop the report generation
    # For example, setting a flag or canceling the task
    try:
        # Handle cancellation of report generation
        cancel_generation_flag = True  # Set a flag to stop the generation process
        return jsonify({"status": "canceled", "message": "Report generation canceled"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
