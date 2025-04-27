# --- START OF FILE app.py (Updated) ---
import os
from flask import Flask, request, jsonify, render_template, send_from_directory
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__, static_folder='.', static_url_path='') # Serve static files from root

# --- API Endpoint for Registration ---
@app.route('/register', methods=['POST'])
def handle_registration():
    """
    Handles the POST request from the NB signup form.
    Receives JSON data, logs it, and returns a success response.
    """
    if not request.is_json:
        logging.warning("Received non-JSON request to /register")
        return jsonify({"status": "error", "message": "Request must be JSON"}), 400

    data = request.get_json()
    logging.info(f"Received registration data: {data}")

    # --- Data Validation (Basic Example) ---
    required_fields = ['role', 'fullName', 'email', 'mobile']
    missing_fields = [field for field in required_fields if field not in data or not data[field]]

    if missing_fields:
        logging.warning(f"Missing required fields: {', '.join(missing_fields)}")
        return jsonify({
            "status": "error",
            "message": f"Missing required fields: {', '.join(missing_fields)}"
        }), 400

    # --- Role-Specific Validation (Example) ---
    role = data.get('role')
    if role == 'student' and not data.get('grade'):
        logging.warning("Missing 'grade' for student role.")
        pass # Making it optional for this example
    elif role == 'educator' and (not data.get('subject') or not data.get('experience')):
        logging.warning("Missing 'subject' or 'experience' for educator role.")
        pass
    elif role == 'parent' and (not data.get('childName') or not data.get('childGrade')):
        logging.warning("Missing 'childName' or 'childGrade' for parent role.")
        pass

    # --- Simulate Database Interaction (Replace with actual DB logic) ---
    try:
        logging.info(f"Simulating saving data for user: {data.get('email')}")
        pass # Placeholder for actual database saving
    except Exception as e:
        logging.error(f"Error processing/saving registration data: {e}", exc_info=True)
        return jsonify({"status": "error", "message": "Internal server error during registration"}), 500

    # --- Return Success Response ---
    return jsonify({
        "status": "success",
        "message": f"Registration received successfully for {data.get('fullName')} as a {data.get('role')}!"
    }), 200

# --- Route to Serve the HTML Page ---
@app.route('/')
def index():
    """Serves the main HTML file."""
    # Serve index.html by default now
    html_filename = "index.html"  # <--- YEH LINE BADAL DI GAYI HAI
    logging.info(f"Serving file: {html_filename}")
    # Use send_from_directory for security and correct path handling
    # Serve from the same directory where app.py is located
    return send_from_directory('.', html_filename)

# --- Main Execution ---
if __name__ == '__main__':
    # Use environment variable for port or default to 5001
    port = int(os.environ.get('PORT', 5001)) # Replit usually sets the PORT env variable automatically
    # Set debug=True for development (auto-reloads), False for production
    # Use host='0.0.0.0' to make it accessible on your network and required by Replit
    logging.info(f"Starting Flask server on http://0.0.0.0:{port}")
    app.run(host='0.0.0.0', port=port, debug=True)

# --- END OF FILE app.py (Updated) ---