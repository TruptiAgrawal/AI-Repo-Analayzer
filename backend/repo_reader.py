from github_service import get_file_content

# These are the files most likely to explain what a project does
PRIORITY_FILES = [
    "main.py", "app.py", "index.py",
    "server.py", "index.js", "main.js",
    "src/main.py", "src/app.py", "src/index.js"
]

# Config files that help understand project setup
CONFIG_FILES = [
    "package.json", "requirements.txt", "pyproject.toml",
    "Cargo.toml", "go.mod", "pom.xml"
]

MAX_FILE_SIZE = 5000  # Characters per file
MAX_FILES = 5  # Maximum files to analyze

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

def get_multiple_sample_files(owner: str, repo: str, file_tree: list) -> list[dict]:
    """
    Analyzes multiple important files from the repository.
    Returns list of dicts with file path and content.
    """
    analyzed_files = []
    
    # 1. Get main entry point file
    for priority in PRIORITY_FILES:
        if priority in file_tree and len(analyzed_files) < MAX_FILES:
            content = get_file_content(owner, repo, priority)
            if content:
                analyzed_files.append({
                    "path": priority,
                    "content": content[:MAX_FILE_SIZE],
                    "type": "entry_point"
                })
                break
    
    # 2. Get config file
    for config in CONFIG_FILES:
        if config in file_tree and len(analyzed_files) < MAX_FILES:
            content = get_file_content(owner, repo, config)
            if content:
                analyzed_files.append({
                    "path": config,
                    "content": content[:MAX_FILE_SIZE],
                    "type": "config"
                })
                break
    
    # 3. Get additional important code files
    code_extensions = [".py", ".js", ".ts", ".go", ".rs", ".java"]
    for path in file_tree:
        if len(analyzed_files) >= MAX_FILES:
            break
        
        # Skip if already analyzed
        if any(f["path"] == path for f in analyzed_files):
            continue
        
        # Look for important patterns in path
        if any(ext in path for ext in code_extensions):
            # Prioritize files with important keywords
            important_keywords = ["service", "handler", "controller", "model", "util", "helper"]
            if any(keyword in path.lower() for keyword in important_keywords):
                content = get_file_content(owner, repo, path)
                if content:
                    analyzed_files.append({
                        "path": path,
                        "content": content[:MAX_FILE_SIZE],
                        "type": "supporting"
                    })
    
    return analyzed_files if analyzed_files else [{"path": "none", "content": "No readable files found.", "type": "error"}]