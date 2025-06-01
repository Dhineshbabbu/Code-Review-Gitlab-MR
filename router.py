from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route("/main")
def main_page():
    return "Welcome to the main page!"

@app.route('/gitlab-webhook', methods=['POST'])
def gitlab_webhook():
    data = request.json

    # Check if it's a merge request event
    if data.get('object_kind') == 'merge_request':
        mr_data = data['object_attributes']
        action = mr_data.get('action')
        state = mr_data.get('state')

        print("Received GitLab merge request event:")
        print(f"Action: {action}, State: {state}")
        print(mr_data)

        if action == 'merge' and state == 'merged':
            print("✅ A merge request was merged!")
            # You can trigger your custom logic here
            # e.g., deploy, notify, run CI, etc.

    return jsonify({'status': 'Received'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)