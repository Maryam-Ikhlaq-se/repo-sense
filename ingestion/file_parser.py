"""
Layer: Ingestion
Responsibility: Filter raw files down to only relevant source code files.
Receives raw file list from github_fetcher, does not fetch anything itself.
"""

SUPPORTED_EXTENSIONS = {'.py', '.js', '.ts', '.java', '.go', '.cs'}
MAX_FILE_SIZE_LINES = 1000


def filter_code_files(files: list[dict]) -> list[dict]:
    """
    Filters raw file list down to meaningful source code files only.

    Args:
        files (list[dict]): Raw file list from github_fetcher

    Returns:
        list[dict]: Each dict has 'path', 'content', 'line_count'
    """

    filtered = []

    for file in files:
        path    = file['path']
        content = file['content']

        # Skip unsupported file types
        if not any(path.endswith(ext) for ext in SUPPORTED_EXTENSIONS):
            continue

        # Skip empty files
        if len(content.strip()) == 0:
            continue

        lines = content.splitlines()

        # Skip oversized files
        if len(lines) > MAX_FILE_SIZE_LINES:
            continue

        filtered.append({
            'path':       path,
            'content':    content,
            'line_count': len(lines)
        })

    return filtered