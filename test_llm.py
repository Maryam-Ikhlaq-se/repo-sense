# test_llm.py
# Purpose: Test prompt builder + LLM layer on one real analyzed file

from ingestion.github_fetcher import fetch_repo_files
from ingestion.file_parser import filter_code_files
from analysis.quality_analyzer import analyze_all_files
from llm.prompt_builder import build_file_prompt
from llm.gemini_client import get_structured_response

REPO_URL = "https://github.com/realpython/reader"

print("Fetching and analyzing repo...")
raw_files  = fetch_repo_files(REPO_URL)
code_files = filter_code_files(raw_files)
analyzed   = analyze_all_files(code_files)

# Test on first file only
file = analyzed[0]
print(f"\nAnalyzing: {file['path']}\n")

prompt   = build_file_prompt(file)
response = get_structured_response(prompt)

print("LLM Response:")
print(f"  Purpose:     {response.get('purpose')}")
print(f"  Patterns:    {response.get('patterns')}")
print(f"  Issues:      {response.get('quality_issues')}")
print(f"  Severity:    {response.get('severity')}")
print(f"  Recommendations: {response.get('recommendations')}")