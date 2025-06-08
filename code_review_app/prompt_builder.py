# Prompt builder function
def build_ai_prompt(file_path, code_diff, lang):
    prompt = f"""You are an experienced software engineer reviewing a code change. Please analyze the following {lang} diff:

    <file path="{file_path}">
    {code_diff}
    </file>

    Provide concise, actionable feedback in the following format:
    - Identify bugs or potential errors
    - Suggest naming improvements
    - Mention possible security concerns
    - Recommend best practices

    Return your feedback as a dictionary where keys are line numbers and values are the corresponding review comments.
    If a line has no issues, do not include it in the dictionary.
    If no issues are found at all, return: "✅ No suggestions for this file."

    Only return the structured feedback in the specified format, without any extra explanations.
    """
    return prompt.strip()