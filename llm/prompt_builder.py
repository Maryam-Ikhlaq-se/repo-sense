"""
Layer: LLM
Responsibility: Build structured prompts from analyzed file data.
This module does NOT call the LLM directly.
It only constructs the prompt string that gemini_client will send.
"""


def build_file_prompt(file: dict) -> str:
    """
    Builds a structured prompt for a single analyzed file.

    Args:
        file (dict): Analyzed file dict from quality_analyzer
                     Must contain: path, content, complexity,
                     coupling, comment_density, maintainability

    Returns:
        str: A complete structured prompt ready to send to Gemini
    """

    return f"""
You are a senior software architect reviewing code for quality and design.

FILE: {file['path']}

MEASURED QUALITY METRICS:
- Lines of Code:       {file['line_count']}
- Cyclomatic Complexity: {file['complexity']} (higher = harder to test)
- Coupling (imports):  {file['coupling']} external dependencies
- Comment Density:     {file['comment_density']} (ratio of comments to code)
- Maintainability Index: {file['maintainability']} out of 100

SOURCE CODE:
{file['content']}

Based on the metrics and code above, respond ONLY in this exact JSON format:
{{
    "purpose": "one sentence describing what this file does",
    "patterns": ["list of design patterns or architectural patterns detected"],
    "quality_issues": ["list of specific quality problems found"],
    "severity": "low or medium or high",
    "recommendations": ["list of specific actionable improvements"]
}}

Return JSON only. No explanation. No markdown. No extra text.
"""


def build_summary_prompt(file_analyses: list[dict]) -> str:
    """
    Builds a prompt for overall repo summary from all file analyses.

    Args:
        file_analyses (list[dict]): LLM analysis results for all files

    Returns:
        str: Prompt asking Gemini to summarize the entire repo
    """

    files_summary = ""
    for f in file_analyses:
        files_summary += f"\n- {f['path']}: {f.get('purpose', 'unknown')}"

    return f"""
You are a senior software architect.
You have analyzed all files in a repository.
Here is a summary of each file's purpose:

{files_summary}

Respond ONLY in this exact JSON format:
{{
    "repo_purpose": "one paragraph describing what this entire repo does",
    "architecture": "description of the overall architectural style detected",
    "biggest_risks": ["top 3 quality or architectural risks in this codebase"]
}}

Return JSON only. No explanation. No markdown. No extra text.
"""