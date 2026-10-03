# 🔍 RepoSense — AI-Powered Codebase Intelligence Tool

> Analyze any GitHub repository in seconds. Get architecture insights, quality metrics, and actionable recommendations powered by Google Gemini AI.

---

## 📌 Purpose

Understanding an unfamiliar codebase is one of the most time-consuming tasks in software engineering. A new developer joining a team, a freelancer inheriting client code, or a tech lead reviewing a project,all face the same problem: **it takes hours to understand what a codebase does, how it is structured, and where the risks are.**

**RepoSense solves this.**

Give it any public GitHub repository URL. It fetches the code, measures quality using industry-standard metrics, and uses an LLM to interpret and explain the findings producing a structured, professional report in under a minute.

---

## 🚀 What It Does

**GitHub URL → Fetch Code → Measure Quality → LLM Interpretation → Markdown Report**


RepoSense performs five steps automatically:

1. **Fetches** all source code files from a public GitHub repository
2. **Filters** relevant code files by language and size
3. **Measures** code quality using static analysis metrics
4. **Interprets** findings using Google Gemini AI
5. **Generates** a structured markdown report with actionable insights

---

## 🧠 AI Approach

RepoSense uses **LLM-Augmented Static Code Analysis** — not pure AI guessing.

| Step | Method |
|------|--------|
| Code fetching | GitHub REST API |
| Quality measurement | Radon library (static analysis) |
| Interpretation | Google Gemini 3.8 Flash (LLM) |
| Output | Structured JSON → Markdown report |

**Key principle:** The LLM is given measured, factual metrics — not just raw code. This grounds the AI interpretation in data, reducing hallucination and increasing accuracy.

---

## 📊 Quality Metrics Analyzed

| Metric | What It Measures | Why It Matters |
|--------|-----------------|----------------|
| **Cyclomatic Complexity** | Number of decision paths in a function | High = hard to test and maintain |
| **Coupling** | Number of external imports | High = hard to change without breaking things |
| **Comment Density** | Ratio of comments to code | Low = poor documentation |
| **Maintainability Index** | Industry standard score (0–100) | Lower = harder to maintain |
| **Lines of Code** | File size | Oversized files signal poor modularity |
| **Test Detection** | Presence of test files | Missing tests = high deployment risk |

---

## 📁 Project Structure

repo-sense/
│
├── ingestion/ # Layer 1 — Data fetching
│ ├── github_fetcher.py # Fetches repo files via GitHub API
│ └── file_parser.py # Filters relevant source code files
│
├── analysis/ # Layer 2 — Quality measurement
│ └── quality_analyzer.py # Computes static quality metrics
│
├── llm/ # Layer 3 — AI interpretation
│ ├── prompt_builder.py # Builds structured prompts
│ └── gemini_client.py # Calls Google Gemini API
│
├── output/ # Layer 4 — Report generation
│ └── report_generator.py # Assembles markdown report
│
├── main.py # Entry point — connects all layers
├── .env # API key (not committed)
├── .env.example # Template for API key setup
└── README.md # This file
---

## 🏗️ Architecture

RepoSense follows a strict **Layered Architecture** pattern:

[ Output Layer ] ← Formats and saves report
↑
[ LLM Layer ] ← Interprets metrics using Gemini AI
↑
[ Analysis Layer ] ← Measures code quality statically
↑
[ Ingestion Layer ] ← Fetches raw data from GitHub


Each layer has a single responsibility and communicates only with the layer directly below it — following **SOLID principles** taught in Software Design & Architecture.

---

## 📋 Sample Output

Running RepoSense on any repository produces a `report.md` file:
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
File-by-File Analysis
🟡 src/reader/feed.py

Purpose: Handles RSS feed fetching and XML parsing
Complexity: 10.0 | Coupling: 4 | Maintainability: 71.36

Quality Issues:

Missing error handling for malformed XML
Function parse_feed() has too many responsibilities

Recommendations:

Split parse_feed() into smaller single-purpose functions
Add try/except around XML parsing logic


---

## 🎯 Real-World Applications

### For Pakistani Software Houses
- **Onboarding acceleration** — New developers understand codebases in minutes, not weeks
- **Client code audits** — Quickly assess quality of inherited or outsourced code
- **Pre-delivery quality checks** — Run before handing code to clients

### For Freelancers
- **Due diligence** — Assess a codebase before taking on a project
- **Quality signaling** — Show clients a professional audit report

### For Tech Leads & Engineering Managers
- **Automated code review support** — Identify high-risk files before review
- **Technical debt visibility** — Quantify and communicate code quality issues

### For Students & Researchers
- **Learning tool** — Understand how professional codebases are structured
- **Research baseline** — Benchmark code quality across open source projects

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.10+
- Google Gemini API key (free tier available at [aistudio.google.com](https://aistudio.google.com))

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/repo-sense.git
cd repo-sense

# Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# Install dependencies
pip install google-genai requests radon python-dotenv

# Configure API key
cp .env.example .env
# Add your Gemini API key to .env
```

### Usage

```bash
python main.py https://github.com/owner/repository
```

Report is saved as `report.md` in the project root.

---

## 🔬 Academic Context

This project is developed as part of a **Master's in Software Engineering** Final Year Project.

**Research Question:**
> Does combining LLM interpretation with static code quality metrics produce more accurate and actionable codebase analysis than either approach alone?

**Courses Applied:**
- **Software Design & Architecture** — Layered architecture, SOLID principles, design patterns
- **Software Quality Engineering** — ISO/IEC 25010 quality attributes, cyclomatic complexity, maintainability index

---

## 🗺️ Future Roadmap

- [ ] RAG-based querying — "What does the auth module do?"
- [ ] Support for private repositories via GitHub token
- [ ] Web UI for non-technical users
- [ ] CI/CD integration — run on every pull request
- [ ] Multi-language support expansion
- [ ] Historical trend tracking — quality over time

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.11 | Core language |
| Google Gemini 3.8 Flash | LLM interpretation |
| Radon | Static code analysis |
| Requests | GitHub API calls |
| Python-dotenv | Environment variable management |

---
---

## 🗺️ Planned Enhancements

### 1. Severity Scoring System
Replace subjective low/medium/high LLM rating with a weighted mathematical formula:
- Combined score from complexity, coupling, and maintainability index
- Overall codebase health score from 0–100
- Measurable, consistent, and academically defensible

### 2. Web Interface
Replace CLI with a browser-based interface built on FastAPI:
- Paste any GitHub URL into the browser
- View the full analysis report on screen
- Download report as markdown or PDF

### 3. CI/CD Integration
GitHub Action that runs RepoSense automatically on every pull request:
- Quality report posted as a PR comment
- Blocks merge if health score drops below threshold
- Zero manual effort for engineering teams

---

## 🔬 Further Research Directions

### Human vs AI Accuracy Benchmark
Measure how RepoSense compares to manual expert review:
- Have experienced developers analyze the same codebases manually
- Compare findings for accuracy, completeness, and time taken
- Quantify the value of LLM-augmented static analysis

### RAG-Based Codebase Q&A
Enable natural language queries over the analyzed repository:
- Index codebase into a vector database
- Answer questions like "Where is authentication handled?"
- Return specific file and line references

### Historical Quality Tracking
Track codebase quality trends across commits over time:
- Detect quality regressions automatically
- Visualize maintainability trends per module
- Alert teams when technical debt accumulates

### Evaluation Framework
Formal LLM output evaluation using RAGAS:
- Build ground truth dataset from expert-reviewed codebases
- Score LLM accuracy, relevance, and faithfulness
- Establish baseline benchmarks for future research

## 👩‍💻 Author
Developed by **Maryam Ikhlaq**
