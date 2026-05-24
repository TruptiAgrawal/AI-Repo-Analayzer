def build_summary_prompt(readme: str, file_tree: list, sample_code: str) -> str:
    """
    Builds a structured prompt so Grok understands exactly what to do.
    Think of this as writing a brief for the AI.
    """
    file_list = "\n".join(file_tree[:40])  # Limit to first 40 files

    prompt = f"""
    
You are a helpful assistant that explains GitHub repositories to beginners.

Here is the information about this repository:

--- README ---
{readme[:3000]}

--- FILE STRUCTURE ---
{file_list}

--- SAMPLE CODE (main file) ---
{sample_code[:2000]}

Please provide:
1. A simple summary of what this project does (2-3 sentences)
2. The folder structure explained simply
3. What the main code does, in plain English

Keep your explanation beginner-friendly.
"""
    return prompt