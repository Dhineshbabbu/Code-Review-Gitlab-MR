# app.py

import os
import json
from flask import Flask, request, jsonify

from google.cloud.aiplatform_v1.services.prediction_service import PredictionServiceClient
from google.cloud.aiplatform_v1.types import PredictRequest

# ────── CONFIG ────────────────────────────────────────────────────────────────
PROJECT_ID   = "agent-development-461516"                   # ← your project
REGION       = "us-central1"                                # ← your region
ENDPOINT_ID  = "5246180093956456448"                    # ← your deployed endpoint
GITLAB_TOKEN = "glpat-U2ZgNMXY1Rs4qe8U_7hv"                   # ← set this as a Secret in Cloud Run
# ────────────────────────────────────────────────────────────────────────────────

app = Flask(__name__)

# 1) Create a PredictionServiceClient via ADC (no key file needed)
client = PredictionServiceClient()

def call_vertex(prompt: str) -> str:
    endpoint = f"projects/{PROJECT_ID}/locations/{REGION}/endpoints/{ENDPOINT_ID}"
    req = PredictRequest(
        endpoint=endpoint,
        instances=[{"content": prompt}],
        # optional: parameters={"temperature": 0.0},
    )
    res = client.predict(request=req)
    # our model returns: {"content": "...feedback text..."}
    return res.predictions[0].get("content", "")

def post_to_gitlab(mr_id, project_id, comment):
    import requests
    url = f"https://gitlab.com/api/v4/projects/{project_id}/merge_requests/{mr_id}/notes"
    headers = {"PRIVATE-TOKEN": GITLAB_TOKEN}
    data = {"body": comment}
    r = requests.post(url, headers=headers, data=data)
    return r.json()

@app.route("/gitlab-webhook", methods=["POST"])
def webhook():
    payload = request.get_json()
    # — extract the MR ID and project ID from GitLab’s webhook payload:
    mr_id      = payload["object_attributes"]["iid"]
    project_id = payload["project"]["id"]
    diff_text  = payload["object_attributes"]["description"]  # or wherever you build your prompt
    
    # 2) Call Vertex AI
    feedback = call_vertex(diff_text)
    
    # 3) Post feedback back into GitLab
    note = post_to_gitlab(mr_id, project_id, feedback)
    
    return jsonify(note), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
