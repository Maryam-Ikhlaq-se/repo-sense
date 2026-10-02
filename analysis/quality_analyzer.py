"""
Layer: Analysis
Responsibility: Extract measurable quality metrics from source code files.
This module does NOT call the LLM. It only computes numbers.
Pure functions — same input always gives same output.
"""

from radon.complexity import cc_visit
from radon.metrics import mi_visit


def analyze_file_quality(file: dict) -> dict:
    """
    Computes quality metrics for a single source code file.

    Args:
        file (dict): A dict with 'path', 'content', 'line_count'
                     from file_parser.filter_code_files()

    Returns:
        dict: Original file data + quality metrics:
              - 'complexity'      (int)  : Average cyclomatic complexity
              - 'coupling'        (int)  : Number of import statements
              - 'comment_density' (float): Ratio of comment lines to total lines
              - 'has_tests'       (bool) : Whether file appears to be a test file
              - 'maintainability' (float): Maintainability index score (0-100)
    """

    content    = file['content']
    path       = file['path']
    lines      = content.splitlines()
    total_lines = file['line_count']

    # --- Metric 1: Cyclomatic Complexity ---
    # Measures number of decision paths (if, for, while, try etc.)
    # Higher = harder to test and maintain
    try:
        complexity_results = cc_visit(content)
        if complexity_results:
            avg_complexity = sum(r.complexity for r in complexity_results) / len(complexity_results)
        else:
            avg_complexity = 1  # No decision paths = simple linear code
    except Exception:
        avg_complexity = 0

    # --- Metric 2: Coupling ---
    # Count how many external modules this file depends on
    # Higher coupling = harder to change without breaking other things
    import_count = sum(
        1 for line in lines
        if line.strip().startswith('import ') or line.strip().startswith('from ')
    )

    # --- Metric 3: Comment Density ---
    # Ratio of comment lines to total lines
    # Low density = poor documentation
    comment_lines = sum(1 for line in lines if line.strip().startswith('#'))
    comment_density = round(comment_lines / total_lines, 2) if total_lines > 0 else 0

    # --- Metric 4: Test File Detection ---
    # Check if this file is a test file by naming convention
    has_tests = 'test' in path.lower() or 'spec' in path.lower()

    # --- Metric 5: Maintainability Index ---
    # Industry standard score 0-100. Higher = more maintainable
    try:
        maintainability = round(mi_visit(content, multi=True), 2)
    except Exception:
        maintainability = 0.0

    return {
        'path':             path,
        'content':          content,
        'line_count':       total_lines,
        'complexity':       round(avg_complexity, 2),
        'coupling':         import_count,
        'comment_density':  comment_density,
        'has_tests':        has_tests,
        'maintainability':  maintainability
    }


def analyze_all_files(files: list[dict]) -> list[dict]:
    """
    Runs quality analysis on all filtered code files.

    Args:
        files (list[dict]): Output from file_parser.filter_code_files()

    Returns:
        list[dict]: Each file dict enriched with quality metrics
    """

    return [analyze_file_quality(file) for file in files]