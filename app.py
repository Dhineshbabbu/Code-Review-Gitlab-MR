from flask import Flask, request, jsonify
import gitlab
import json
import ast
import re
from code_review_app.lang_detector import detect_language_details
from code_review_app.webhook_listener import gitlab_webhook
from code_review_app.prompt_builder import build_ai_prompt
from code_review_app.ai_reviewer import call_vertex_ai_model , initialize_vertex_ai
from code_review_app.post_comment_in_gitlab import post_comment_in_gitlab

app = Flask(__name__)
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
    # feedback_dict = ast.literal_eval(ai_feedback)
    print(ai_feedback)
    print("=" * 40)

    print("Sending the feedback in Gitlab..")
    result = post_comment_in_gitlab(file_path , MERGE_REQUEST_IID , PROJECT_ID , ai_feedback)
    
    return result,200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)  # Run the Flask app on port 5000
