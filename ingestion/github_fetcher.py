# Layer: Ingestion
# Responsibility: Fetch all file paths and raw content from a public GitHub repository.
# This module has no knowledge of analysis, LLM, or output layer
import requests
def fetch_repo_files(repo_url: str) -> list[dict]:
    """
    Fetches all files from a public GitHub repository using the GItHub REST API.
    Args: 
        repo_url (str): Full GitHub URL e.g. 'https://github.com/owner/repo'
    Returns:
        list[dict]: A list of dicts, each containing:
                    'path' (str): Relative file path inside the repo
                    'content' (str): Raw text content of the file
    Raises:
        Exception: If the repository can't be accessed (invalid URL or private repo)
    """
# Extract owner and repo name from the URL
    parts = repo_url.rstrip('/').split('/')
    owner = parts[-2]
    repo = parts[-1]

# GitHub API endpoint to get the full recursive file tree of the repo
    tree_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/HEAD?recursive=1"
    tree_response = requests.get(tree_url, timeout=10)  # for network connectivity issues, using timeout

# Stop early if repo is inaccessible
    if tree_response.status_code != 200:
       raise Exception(f"Failed to fetch repo tree. Status code: {tree_response.status_code}")
    tree = tree_response.json().get('tree',[])
    files = []
    for item in tree:
    # Skip directories we only want actual files (blobs)
      if item['type'] != 'blob':
         continue
    # Build raw content URL for each file
      raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/HEAD/{item['path']}"
      content_response = requests.get(raw_url, timeout=10)  # for network connectivity issues, using timeout

    # Only include files that are successfully fetched
      if content_response.status_code == 200:
        files.append({
            'path': item['path'],
            'content': content_response.text
        })
    return files