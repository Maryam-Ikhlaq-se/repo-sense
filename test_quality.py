# test_quality.py
# Purpose: Test quality analyzer on real fetched code files

from ingestion.github_fetcher import fetch_repo_files
from ingestion.file_parser import filter_code_files
from analysis.quality_analyzer import analyze_all_files

REPO_URL = "https://github.com/realpython/reader"

print("Fetching repo...")
raw_files = fetch_repo_files(REPO_URL)

print("Filtering code files...")
code_files = filter_code_files(raw_files)

print("Analyzing quality...\n")
analyzed = analyze_all_files(code_files)

for f in analyzed:
    print(f"File: {f['path']}")
    print(f"  Lines:           {f['line_count']}")
    print(f"  Complexity:      {f['complexity']}")
    print(f"  Coupling:        {f['coupling']}")
    print(f"  Comment Density: {f['comment_density']}")
    print(f"  Has Tests:       {f['has_tests']}")
    print(f"  Maintainability: {f['maintainability']}")
    print()