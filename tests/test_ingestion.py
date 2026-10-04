# test_ingestion.py
# Purpose: Test ingestion layer end-to-end with a real GitHub repo

from ingestion.github_fetcher import fetch_repo_files
from ingestion.file_parser import filter_code_files

# Small public Python repo for testing
# REPO_URL = "https://github.com/pallets/flask" # it was too mucg time to fetch
REPO_URL = "https://github.com/realpython/reader"

print("Fetching repo files...")
raw_files = fetch_repo_files(REPO_URL)
print(f"Total files found: {len(raw_files)}")

print("\nFiltering code files...")
code_files = filter_code_files(raw_files)
print(f"Code files to analyze: {len(code_files)}")

print("\nFirst 5 files:")
for f in code_files[:5]:
    print(f"  {f['path']} — {f['line_count']} lines")