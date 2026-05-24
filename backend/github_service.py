# talks to github api to fetch repo info 
import httpx
import requests
GITHUB_API = "https://api.github.com"

def parse_repo_url(url: str) -> tuple:
    """
    Handles messy GitHub URLs like:
    - https://github.com/owner/repo
    - https://github.com/owner/repo/tree/main
    - https://github.com/owner/repo/tree/main?search=1
    Always extracts just owner and repo name.
    """
    # Strip query params first (?search=1 etc)
    url = url.split("?")[0]
    
    # Strip trailing slash
    url = url.rstrip("/")
    
    # Split by "/" and grab the parts after "github.com"
    parts = url.split("/")
    
    # Find "github.com" index and grab the next two parts
    try:
        gh_index = parts.index("github.com")
        owner = parts[gh_index + 1]
        repo  = parts[gh_index + 2]
        return owner, repo
    except (ValueError, IndexError):
        raise ValueError(f"Could not parse GitHub URL: {url}")

def get_readme(owner: str, repo: str) -> str:
    """Fetches the README content of a repo."""
    url = f"{GITHUB_API}/repos/{owner}/{repo}/readme"
    headers = {"Accept": "application/vnd.github.raw+json"}
    
    try:
        response = httpx.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            return response.text
        return "No README found."
        
    except httpx.RequestError as e:
        print(f"Network error fetching README: {e}")
        return "Could not fetch README."

def get_file_tree(owner: str, repo: str) -> list:
    """Fetches the full folder/file structure of a repo."""
    url = f"{GITHUB_API}/repos/{owner}/{repo}/git/trees/HEAD?recursive=1"
    
    try:
        response = httpx.get(url, timeout=15)  # ← response is assigned FIRST
        
        if response.status_code == 200:
            tree = response.json().get("tree", [])
            return [item["path"] for item in tree if item["type"] == "blob"]
        else:
            print(f"GitHub API error: {response.status_code} - {response.text}")
            return []
            
    except httpx.RequestError as e:
        print(f"Network error fetching file tree: {e}")
        return []

def get_file_content(owner: str, repo: str, path: str) -> str:
    """
    Reads a specific file inside the repo.
    """
    url = f"{GITHUB_API}/repos/{owner}/{repo}/contents/{path}"
    headers = {"Accept": "application/vnd.github.raw+json"}
    response = httpx.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.text
    return ""   