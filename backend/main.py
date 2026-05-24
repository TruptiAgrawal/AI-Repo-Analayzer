from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from github_service import parse_repo_url, get_readme, get_file_tree
from repo_reader import get_best_sample_file
from prompt_builder import build_summary_prompt
from grok_client import ask_grok

app = FastAPI()

class RepoRequest(BaseModel):
    url: str

@app.post("/analyze")
def analyze_repo(request: RepoRequest):
    try:
        owner, repo = parse_repo_url(request.url)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    readme     = get_readme(owner, repo)
    file_tree  = get_file_tree(owner, repo)
    
    if not file_tree:
        raise HTTPException(
            status_code=404,
            detail=f"Repo '{owner}/{repo}' not found or is empty/private."
        )

    sample_code = get_best_sample_file(owner, repo, file_tree)
    prompt      = build_summary_prompt(readme, file_tree, sample_code)
    answer      = ask_grok(prompt)

    return {
        "summary":   answer,
        "file_tree": file_tree[:30],
        "repo":      f"{owner}/{repo}"
    }