from flask import Flask, request, jsonify
import requests
from lang_detector import detect_language_details
from webhook_listener import gitlab_webhook

app = Flask(__name__)

@app.route('/gitlab-webhook', methods=['POST'])
def gitlab_webhook_listener():
    changes_summary , file_path = gitlab_webhook()
    lang_detected = detect_language_details(changes_summary,file_path)
    return lang_detected, 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # Run the Flask app on port 5000