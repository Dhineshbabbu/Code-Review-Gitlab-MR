# Prompt builder function
def build_ai_prompt(file_path, code_diff, lang):
    prompt = f"""You are an experienced software engineer reviewing a code change. Please analyze the following {lang} diff:

    <file path="{file_path}">
    {code_diff}
    </file>

    Provide concise, actionable feedback:
    - Identify bugs or potential errors
    - Suggest naming improvements
    - Mention possible security concerns
    - Recommend best practices
    - If no issues found, say: "✅ No suggestions for this file."

    Only respond with the review suggestions and do not add extra explanations.
    """
    return prompt.strip()