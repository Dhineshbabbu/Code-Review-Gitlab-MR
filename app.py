# app.py

import os
import json
from flask import Flask, request, jsonify
from google.cloud import aiplatform
from code_review_app.lang_detector import detect_language_details
from code_review_app.webhook_listener import gitlab_webhook
from code_review_app.prompt_builder import build_ai_prompt
from code_review_app.ai_reviewer import post_comment_in_gitlab

# ─── CONFIG ────────────────────────────────────────────────────────────────────
PROJECT_ID      = "agent-development-461516"
REGION          = "us-central1"
ENDPOINT_ID     = "5246180093956456448"   # ← replace this
# ────────────────────────────────────────────────────────────────────────────────

# Initialize Flask
app = Flask(__name__)

# Initialize Vertex AI client via ADC (no key file needed!)
aiplatform.init(project=PROJECT_ID, location=REGION)

def call_vertex_ai_model(prompt: str) -> str:
    """
    Sends `prompt` to your deployed Vertex AI endpoint and returns the text response.
    """
    endpoint = aiplatform.Endpoint(
        endpoint_name=f"projects/{PROJECT_ID}/locations/{REGION}/endpoints/{ENDPOINT_ID}"
    )
    prediction = endpoint.predict(instances=[{"content": prompt}])
    # adjust this if your model returns a different JSON shape
    return prediction.predictions[0].get("content", "")

@app.route("/gitlab-webhook", methods=["POST"])
def listener():
    # 1) Parse the GitLab webhook payload
    summary, file_path, mr_id, proj_id, gitlab_token = gitlab_webhook()

    # 2) Build the prompt
    lang = detect_language_details(summary, file_path)
    prompt = build_ai_prompt(file_path, summary, lang)

    # 3) Call Vertex AI
    ai_feedback = call_vertex_ai_model(prompt)

    # 4) Post the feedback back into GitLab
    result = post_comment_in_gitlab(
        file_path, mr_id, proj_id, gitlab_token, ai_feedback
    )

    # 5) Return 200 to GitLab
    return jsonify(result), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    # debug=True is fine locally, but disable in production
    app.run(host="0.0.0.0", port=port, debug=True)
