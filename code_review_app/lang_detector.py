from pygments.lexers import guess_lexer, get_lexer_by_name
from pygments.util import ClassNotFound
import os

LANGUAGE_EXTENSIONS = {
    ".py": "Python",
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".java": "Java",
    ".cpp": "C++",
    ".rb": "Ruby",
    ".go": "Go",
    ".rs": "Rust",
    ".php": "PHP",
    ".cs": "C#",
    ".swift": "Swift",
    ".kt": "Kotlin",
    ".m": "Objective-C",
    ".scala": "Scala",
    ".html": "HTML",
    ".css": "CSS",
    ".sql": "SQL",
    ".sh": "Shell Script",
    ".json": "JSON",
    ".yaml": "YAML",
    ".md": "Markdown"
}

code = """
def greet(name: str) -> None:
    print(f"Hello, {name}")
    if name == "Alice":
        print("Welcome back!")
"""

def detect_language_details(code_snippet, file_path=None):
    if file_path:
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        if ext in LANGUAGE_EXTENSIONS:
            return {
                'name': LANGUAGE_EXTENSIONS[ext],
                'slug': LANGUAGE_EXTENSIONS[ext].lower().replace(' ', '-'),
                'extensions': [ext],
                'mime': '',  # Could map MIME types separately if needed
                'confidence': 0.9 if ext else 0.5,
                'source': 'extension'
            }

    try:
        lexer = guess_lexer(code_snippet)
        full_lexer = get_lexer_by_name(lexer.name)
        print(full_lexer.name)
        return full_lexer.name
    except ClassNotFound as e:
        print("ClassNotFound:", e)
        return 'Unknown'
