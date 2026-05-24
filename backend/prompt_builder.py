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

def build_multi_file_prompt(readme: str, file_tree: list, analyzed_files: list[dict]) -> str:
    """
    Builds a prompt with multiple files for deeper analysis.
    """
    file_list = "\n".join(file_tree[:40])
    
    # Format analyzed files
    files_section = ""
    for file_info in analyzed_files:
        files_section += f"\n--- {file_info['path']} ({file_info['type']}) ---\n"
        files_section += file_info['content'][:2000] + "\n"
    
    prompt = f"""
You are a helpful assistant that explains GitHub repositories to beginners.

Here is the information about this repository:

--- README ---
{readme[:3000]}

--- FILE STRUCTURE ---
{file_list}

--- KEY FILES ANALYZED ---
{files_section}

Please provide:
1. A comprehensive summary of what this project does (3-4 sentences)
2. The main technologies and dependencies used
3. How the different files work together (architecture overview)
4. What each key file does, in plain English
5. How someone would get started using this project

Keep your explanation beginner-friendly but thorough.
"""
    return prompt