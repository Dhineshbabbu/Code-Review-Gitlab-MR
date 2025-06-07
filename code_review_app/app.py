from flask import Flask, request, jsonify
import requests
import gitlab

from lang_detector import detect_language_details
from webhook_listener import gitlab_webhook
from prompt_builder import build_ai_prompt
from ai_reviewer import call_vertex_ai_model , initialize_vertex_ai

app = Flask(__name__)
GITLAB_URL = "https://gitlab.com" 


@app.route('/gitlab-webhook', methods=['POST'])
def gitlab_webhook_listener():
    changes_summary , file_path , MERGE_REQUEST_IID , PROJECT_ID , GITLAB_TOKEN= gitlab_webhook()
    lang_detected = detect_language_details(changes_summary,file_path)
    prompt = build_ai_prompt(file_path, changes_summary, lang_detected)
    print("🧠 Sending to AI for analysis...")
    initialize_vertex_ai()
    ai_feedback = call_vertex_ai_model(prompt)
    print("🤖 AI Feedback:")
    print(ai_feedback)
    print("=" * 40)

    print("Sending the feedback in Gitlab..")
    gl = gitlab.Gitlab(GITLAB_URL, private_token=GITLAB_TOKEN)
    
    # Get the project
    project = gl.projects.get(PROJECT_ID)
    # Get the merge request
    mr = project.mergerequests.get(MERGE_REQUEST_IID)
    
    discussion = mr.discussions.create({
        "body": ai_feedback,
        "position": {
            "new_path": file_path,
            "line": 8,
            "line_type": "+"
        }
    })
    print("Comment posted successfully!")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # Run the Flask app on port 5000