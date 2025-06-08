from flask import Flask, request, jsonify
import gitlab
import json
import re
from lang_detector import detect_language_details
from webhook_listener import gitlab_webhook
from prompt_builder import build_ai_prompt
from ai_reviewer import call_vertex_ai_model , initialize_vertex_ai
from post_comment_in_gitlab import post_comment_in_gitlab

app = Flask(__name__)
@app.route('/gitlab-webhook', methods=['POST'])
def gitlab_webhook_listener():
    changes_summary , file_path , MERGE_REQUEST_IID , PROJECT_ID , GITLAB_TOKEN= gitlab_webhook()
    lang_detected = detect_language_details(changes_summary,file_path)
    prompt = build_ai_prompt(file_path, changes_summary, lang_detected)
    
    print("🧠 Sending to AI for analysis...")
    initialize_vertex_ai()
    ai_feedback = call_vertex_ai_model(prompt)
    
    print("🤖 AI Feedback:");print(ai_feedback)
    pattern = r'(\d+): "- \[(.*?)\](.*?)"'
    matches = re.findall(pattern, ai_feedback)
    feedback_dict = {}
    for key, category, message in matches:
        key = int(key)  # Convert key to integer
        if key in feedback_dict:
            feedback_dict[key].append((category, message))
        else:
            feedback_dict[key] = [(category, message)]

    # Pretty-print the resulting dictionary
    formatted_dict = json.dumps(feedback_dict, indent=4)
    print(formatted_dict)
    print("=" * 40)

    print("Sending the feedback in Gitlab..")
    result = post_comment_in_gitlab(file_path , MERGE_REQUEST_IID , PROJECT_ID , formatted_dict)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # Run the Flask app on port 5000