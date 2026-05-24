from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from github_service import parse_repo_url, get_readme, get_file_tree
from repo_reader import get_best_sample_file, get_multiple_sample_files
from prompt_builder import build_summary_prompt, build_multi_file_prompt
from grok_client import ask_grok

app = FastAPI()

class RepoRequest(BaseModel):
    url: str
    multi_file: bool = True  # Enable multi-file analysis by default

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

    # Use multi-file analysis if requested
    if request.multi_file:
        analyzed_files = get_multiple_sample_files(owner, repo, file_tree)
        prompt = build_multi_file_prompt(readme, file_tree, analyzed_files)
        analyzed_file_paths = [f["path"] for f in analyzed_files]
    else:
        sample_code = get_best_sample_file(owner, repo, file_tree)
        prompt = build_summary_prompt(readme, file_tree, sample_code)
        analyzed_file_paths = []
    
    answer = ask_grok(prompt)

    return {
        "summary": answer,
        "file_tree": file_tree[:30],
        "repo": f"{owner}/{repo}",
        "analyzed_files": analyzed_file_paths
    }