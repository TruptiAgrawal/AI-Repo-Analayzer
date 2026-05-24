from github_service import get_file_content

# These are the files most likely to explain what a project does
PRIORITY_FILES = [
    "main.py", "app.py", "index.py",
    "server.py", "index.js", "main.js",
    "src/main.py", "src/app.py"
]

def get_best_sample_file(owner: str, repo: str, file_tree: list) -> str:
    """
    MCP Tool: Picks the most useful file to show the AI.
    Looks for common entry-point files first.
    """
    for priority in PRIORITY_FILES:
        if priority in file_tree:
            content = get_file_content(owner, repo, priority)
            if content:
                return content

    # Fallback: grab the first .py or .js file found
    for path in file_tree:
        if path.endswith(".py") or path.endswith(".js"):
            return get_file_content(owner, repo, path)

    return "No readable code file found."