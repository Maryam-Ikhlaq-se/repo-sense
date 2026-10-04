# RepoSense AI-Powered Codebase Intelligence Tool

RepoSense analyzes any public GitHub repository and produces a structured quality report. It combines static code analysis with LLM interpretation to give developers actionable insights about architecture, code quality, and technical risks.

---

## Purpose

Understanding an unfamiliar codebase is one of the most time-consuming tasks in software engineering. New team members, freelancers inheriting client code, and tech leads reviewing projects all face the same problem: it takes hours to understand what a codebase does, how it is structured, and where the risks are.

RepoSense solves this by automating that analysis.

---

## How It Works

GitHub URL → Fetch Code → Measure Quality → LLM Interpretation → Markdown Report


1. Fetches all source code files from a public GitHub repository
2. Filters relevant code files by language and size
3. Measures code quality using static analysis metrics
4. Interprets findings using Google Gemini AI
5. Generates a structured markdown report with actionable insights

---

## AI Approach

RepoSense uses LLM-Augmented Static Code Analysis.

| Step | Method |
|------|--------|
| Code fetching | GitHub REST API |
| Quality measurement | Radon library (static analysis) |
| Interpretation | Google Gemini 3.8 Flash |
| Output | Structured JSON parsed into Markdown |

The LLM is given measured, factual metrics rather than raw code alone. This grounds the interpretation in data and reduces hallucination.

---

## Quality Metrics

| Metric | What It Measures | Why It Matters |
|--------|-----------------|----------------|
| Cyclomatic Complexity | Decision paths in a function | High values are hard to test and maintain |
| Coupling | External imports per file | High coupling breaks easily when dependencies change |
| Comment Density | Ratio of comments to code lines | Low density signals poor documentation |
| Maintainability Index | Industry standard score 0 to 100 | Lower scores indicate harder to maintain code |
| Lines of Code | File size | Oversized files indicate poor modularity |
| Test Detection | Presence of test files | Missing tests signal high deployment risk |

---

## Project Structure

```
repo-sense/
│
├── ingestion/                  # Layer 1 — Data fetching
│   ├── github_fetcher.py       # Fetches repo files via GitHub API
│   └── file_parser.py          # Filters relevant source code files
│
├── analysis/                   # Layer 2 — Quality measurement
│   └── quality_analyzer.py     # Computes static quality metrics
│
├── llm/                        # Layer 3 — AI interpretation
│   ├── prompt_builder.py       # Builds structured prompts
│   └── gemini_client.py        # Calls Google Gemini API
│
├── output/                     # Layer 4 — Report generation
│   └── report_generator.py     # Assembles markdown report
│
├── tests/                      # All test files
│   ├── test_connection.py
│   ├── test_ingestion.py
│   ├── test_llm.py
│   └── test_quality.py
│
├── main.py                     # Entry point — connects all layers
├── .env                        # API key (not committed)
├── .env.example                # Template for API key setup
└── README.md                   # This file
```
---

## Architecture

RepoSense follows a strict **Layered Architecture** pattern where each layer has a single responsibility and communicates only with the layer directly below it.
```
[ Output Layer ] ← Formats and saves the report
↑
[ LLM Layer ] ← Interprets metrics using Gemini
↑
[ Analysis Layer ] ← Measures code quality statically
↑
[ Ingestion Layer ] ← Fetches raw data from GitHub
```

This follows SOLID principles applied in Software Design and Architecture.

---

## Sample Output

RepoSense Analysis Report
Repository: https://github.com/owner/repo
Analyzed At: 2026-10-01 23:00
Total Files Analyzed: 6

Repository Overview
Purpose: A command-line RSS feed reader that fetches, parses,
and displays articles from configured feed URLs.

Architecture: Layered architecture with clear separation between
feed parsing, data storage, and presentation layers.

Biggest Risks:

No error handling for network failures during feed fetch
High cyclomatic complexity in feed.py parsing logic
Missing unit tests for core feed processing functions

File: src/reader/feed.py
Purpose: Handles RSS feed fetching and XML parsing
Complexity: 10.0 | Coupling: 4 | Maintainability: 71.36

Quality Issues:

Missing error handling for malformed XML
Function parse_feed() has too many responsibilities

Recommendations:

Split parse_feed() into smaller single-purpose functions
Add try/except around XML parsing logic

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.11 | Core language |
| Google Gemini 3.8 Flash | LLM interpretation |
| Radon | Static code analysis |
| Requests | GitHub API calls |
| python-dotenv | Environment variable management |

---
## Setup

Prerequisites: Python 3.10 or higher, Google Gemini API key from aistudio.google.com

```bash
git clone https://github.com/yourusername/repo-sense.git
cd repo-sense

python -m venv venv
venv\Scripts\activate

pip install google-genai requests radon python-dotenv

cp .env.example .env
# Add your Gemini API key to .env
```

```bash
python main.py https://github.com/owner/repository
```

The report is saved as `report.md` in the project root.

---

## Academic Context

Developed as part of BS Software Engineering semester project.

Research Question: Does combining LLM interpretation with static code quality metrics produce more accurate and actionable codebase analysis than either approach alone?

Courses applied:
- Software Design and Architecture (Layered architecture, SOLID principles, design patterns)
- Software Quality Engineering  (ISO/IEC 25010 quality attributes, cyclomatic complexity, maintainability index)
- Applied prompt engineering and context grounding techniques for LLM-based code analysis.

---

## Planned Enhancements

### Severity Scoring System
Replace the subjective low/medium/high LLM rating with a weighted mathematical formula combining complexity, coupling, and maintainability into a single codebase health score from 0 to 100.

### Web Interface
A browser-based interface built on FastAPI where users paste a GitHub URL, view the analysis on screen, and download the report as markdown or PDF.

### CI/CD Integration
A GitHub Action that runs RepoSense automatically on every pull request, posts the quality report as a PR comment, and optionally blocks merges if the health score drops below a defined threshold.

---

## Further Research Directions

### Human vs AI Accuracy Benchmark
Compare RepoSense findings against manual expert reviews on the same codebases to quantify the value of LLM-augmented static analysis.

### RAG-Based Codebase Q&A
Index the codebase into a vector database to enable natural language queries such as "Where is authentication handled?" with specific file and line references returned.

### Historical Quality Tracking
Track codebase quality trends across commits to detect regressions automatically and visualize maintainability over time.

### Evaluation Framework
Formal LLM output evaluation using RAGAS with a ground truth dataset built from expert-reviewed codebases.

---

## Author

Developed by Maryam Ikhlaq 
