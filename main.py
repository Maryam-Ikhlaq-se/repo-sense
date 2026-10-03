"""
RepoSense — AI-Powered Codebase Intelligence Tool
Main entry point: connects all layers end-to-end.

Usage:
    python main.py <github_repo_url>

Example:
    python main.py https://github.com/realpython/reader
"""

import sys
from ingestion.github_fetcher import fetch_repo_files
from ingestion.file_parser import filter_code_files
from analysis.quality_analyzer import analyze_all_files
from llm.prompt_builder import build_file_prompt, build_summary_prompt
from llm.gemini_client import get_structured_response
from output.report_generator import generate_report, save_report


def main(repo_url: str):

    # --- Step 1: Ingestion ---
    print(f"\n[1/5] Fetching repo: {repo_url}")
    raw_files  = fetch_repo_files(repo_url)
    code_files = filter_code_files(raw_files)
    print(f"      Found {len(code_files)} code files to analyze")

    # --- Step 2: Quality Analysis ---
    print("\n[2/5] Running quality analysis...")
    analyzed = analyze_all_files(code_files)

    # --- Step 3: LLM File Analysis ---
    print("\n[3/5] Getting LLM interpretation for each file...")
    llm_results = []
    for file in analyzed:
        print(f"      Analyzing: {file['path']}")
        prompt   = build_file_prompt(file)
        result   = get_structured_response(prompt)
        result['path'] = file['path']
        llm_results.append(result)

    # --- Step 4: LLM Repo Summary ---
    print("\n[4/5] Generating overall repo summary...")
    summary_prompt = build_summary_prompt(llm_results)
    repo_summary   = get_structured_response(summary_prompt)

    # --- Step 5: Report Generation ---
    print("\n[5/5] Generating report...")
    report      = generate_report(repo_url, analyzed, llm_results, repo_summary)
    output_path = save_report(report)

    print(f"\n✅ Report saved to: {output_path}")
    print("   Open report.md to see full analysis.\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <github_repo_url>")
        sys.exit(1)

    main(sys.argv[1])