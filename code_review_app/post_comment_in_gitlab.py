import gitlab

GITLAB_URL = 'https://gitlab.com' 
PRIVATE_TOKEN = 'glpat-Fpx6UpP3rTdJ3PHoycB8'

def post_comment_in_gitlab(FILE_PATH , MERGE_REQUEST_IID , PROJECT_ID  , COMMENT_TEXT):
    
    # --- Authentication ---
    gl = gitlab.Gitlab(GITLAB_URL, private_token=PRIVATE_TOKEN)
    
    # --- Get Project and MR ---
    project = gl.projects.get(PROJECT_ID)
    mr = project.mergerequests.get(MERGE_REQUEST_IID)

    note = mr.notes.create({'body':COMMENT_TEXT})
       
    # for line_number, comment in COMMENT_TEXT.items():
    #     # --- Authentication ---
    #     gl = gitlab.Gitlab(GITLAB_URL, private_token=PRIVATE_TOKEN)

    #     # --- Get Project and MR ---
    #     project = gl.projects.get(PROJECT_ID)
    #     mr = project.mergerequests.get(MERGE_REQUEST_IID)

    #     # --- Get diff_refs ---
    #     diff_refs = mr.diff_refs  # This should be a dict
    #     base_sha = diff_refs['base_sha']
    #     head_sha = diff_refs['head_sha']
    #     start_sha = diff_refs.get('start_sha', base_sha)

    #     # --- Prepare position ---
    #     position_data = {
    #         'position': {
    #             'base_sha': base_sha,
    #             'start_sha': start_sha,
    #             'head_sha': head_sha,
    #             'old_path': FILE_PATH,
    #             'new_path': FILE_PATH,
    #             'position_type': 'text',
    #             'line_code': f"{base_sha}_{line_number}_{line_number}",
    #             'old_line': None,
    #             'new_line': line_number,  # Adjusted to match the diff
    #             'line_type': "new",  # Explicitly set to "new"
    #             'line_range': {
    #                 'start': {
    #                     'line_code': f"{base_sha}_{line_number}_{line_number}",
    #                     'type': "new",
    #                     'old_line': None,
    #                     'new_line': line_number
    #                 },
    #                 'end': {
    #                     'line_code': f"{base_sha}_{line_number}_{line_number}",
    #                     'type': "new",
    #                     'old_line': None,
    #                     'new_line': line_number
    #                 }
    #             },
    #             'ignore_whitespace_change': False
    #         }
    #     }

    #     note_data = {
    #         'body': comment,
    #         **position_data
    #     }

    #     # --- Resend the Comment ---
    #     try:
    #         discussion = mr.discussions.create(note_data)
    #         print(f"✅ Comment added successfully for line {line_number}!")
    #     except Exception as e:
    #         print(f"❌ Failed to add comment for line {line_number}: {e}")
    return "Comments posted successfully"
