from flask import Flask, request, jsonify
import requests

# GitLab project info and token
GITLAB_TOKEN = "glpat-Fpx6UpP3rTdJ3PHoycB8"  # Replace with your actual token
def gitlab_webhook():
    data = request.json

    # Check if it's a merge request event
    if data.get('object_kind') == 'merge_request':
        mr_data = data['object_attributes']
        action = mr_data.get('action')
        state = mr_data.get('state')

        MERGE_REQUEST_IID = mr_data.get('iid')
        PROJECT_ID = mr_data.get('source_project_id')  # Get project ID from the merge request data
        if not PROJECT_ID:
            print("❌ Project ID not found in the merge request data.")
            return jsonify({'status': 'Error', 'message': 'Project ID not found'}), 400
        PROJECT_AUTHOR = mr_data['last_commit']['author']
        source_branch = mr_data.get('source_branch')
        target_branch = mr_data.get('target_branch')

        print("Received GitLab merge request event:")
        print(f"Action: {action}, State: {state}") 
        print(f"Fetching diff between {target_branch} → {source_branch}...")
        chnages_summary , file_path = fetch_and_print_diff(source_branch, target_branch,PROJECT_ID)

            # Get source and target branch from the merge request
            # source_branch = mr_data.get('source_branch')
            # target_branch = mr_data.get('target_branch')

    return chnages_summary , file_path , MERGE_REQUEST_IID , PROJECT_ID , GITLAB_TOKEN


def fetch_and_print_diff(source_branch, target_branch,PROJECT_ID):
    url = f"https://gitlab.com/api/v4/projects/{PROJECT_ID}/repository/compare" 
    params = {
        "from": target_branch,  # base branch
        "to": source_branch      # feature branch
    }

    headers = {
        "PRIVATE-TOKEN": GITLAB_TOKEN
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        diff_data = response.json()
        print("\n📄 File Diffs:\n")

        for diff in diff_data.get('diffs', []):
            file_path = diff['new_path']
            change_summary = diff['diff']
            print(f"File: {file_path}")
            print(change_summary)
            print("-" * 40)
    else:
        print("❌ Failed to fetch diff:", response.status_code, response.text)
        
    return change_summary , file_path
