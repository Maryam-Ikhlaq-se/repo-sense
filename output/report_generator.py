"""
Layer: Output
Responsibility: Assemble all analyzed file results into a clean markdown report.
This module does NOT fetch, analyze, or call LLM.
It only formats and writes the final report.
"""

import os
from datetime import datetime


def generate_report(repo_url: str, file_analyses: list[dict], llm_results: list[dict], repo_summary: dict) -> str:
    """
    Assembles a full markdown report from all analysis results.

    Args:
        repo_url      (str)       : The GitHub repo URL that was analyzed
        file_analyses (list[dict]): Quality metrics from quality_analyzer
        llm_results   (list[dict]): LLM interpretations from gemini_client
        repo_summary  (dict)      : Overall repo summary from LLM

    Returns:
        str: Full markdown report as a string
    """

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    # --- Report Header ---
    report = f"""# RepoSense Analysis Report

**Repository:** {repo_url}
**Analyzed At:** {timestamp}
**Total Files Analyzed:** {len(file_analyses)}

---

## Repository Overview

**Purpose:**
{repo_summary.get('repo_purpose', 'N/A')}

**Architecture:**
{repo_summary.get('architecture', 'N/A')}

**Biggest Risks:**
"""
    for risk in repo_summary.get('biggest_risks', []):
        report += f"- {risk}\n"

    report += "\n---\n\n## File-by-File Analysis\n"

    # --- Per File Section ---
    for metrics, llm in zip(file_analyses, llm_results):
        severity_emoji = {"low": "🟢", "medium": "🟡", "high": "🔴"}.get(
            llm.get('severity', 'low'), "🟢"
        )

        report += f"""
### {severity_emoji} `{metrics['path']}`

**Purpose:** {llm.get('purpose', 'N/A')}

**Quality Metrics:**
| Metric | Value |
|--------|-------|
| Lines of Code | {metrics['line_count']} |
| Cyclomatic Complexity | {metrics['complexity']} |
| Coupling (imports) | {metrics['coupling']} |
| Comment Density | {metrics['comment_density']} |
| Maintainability Index | {metrics['maintainability']} |
| Has Tests | {metrics['has_tests']} |

**Design Patterns Detected:**
"""
        for pattern in llm.get('patterns', []):
            report += f"- {pattern}\n"

        report += "\n**Quality Issues:**\n"
        for issue in llm.get('quality_issues', []):
            report += f"- {issue}\n"

        report += "\n**Recommendations:**\n"
        for rec in llm.get('recommendations', []):
            report += f"- {rec}\n"

        report += "\n---\n"

    return report


def save_report(report: str, output_path: str = "report.md") -> str:
    """
    Saves the generated report to a markdown file.

    Args:
        report      (str): Full markdown report string
        output_path (str): File path to save the report

    Returns:
        str: Absolute path where report was saved
    """

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)

    return os.path.abspath(output_path)