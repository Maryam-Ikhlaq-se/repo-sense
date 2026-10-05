# My Learning Journal 

Revision notes covering core concepts, errors, bugs, and techniques
learned during project development.
---
## Project  RepoSense

AI-Powered Codebase Intelligence Tool.
Analyzes any public GitHub repository and produces a structured quality report
combining static analysis with LLM interpretation.
---

## Core Concepts

### 1. Layered Architecture

Code organized into strict layers where each layer has one job and only
communicates with the layer directly below it.

```
[ Output Layer    ]   ← Formats and saves report
        ↑
[ LLM Layer       ]   ← AI interpretation
        ↑
[ Analysis Layer  ]   ← Quality measurement
        ↑
[ Ingestion Layer ]   ← Data fetching
```

Rule: Ingestion never calls LLM. LLM never fetches from GitHub.
Analysis never formats output. Each layer is independently replaceable.

Why it matters: Without layers, one change breaks everything.
With layers, swap the LLM provider and zero other files change.

---

### 2. Single Responsibility Principle (SRP)

Every module, class, or function does exactly one thing.
If you need "and" to describe it — it violates SRP.

```python
# Wrong — three jobs in one function
def fetch_and_analyze_and_summarize(repo_url): ...

# Correct — one job each
def fetch_repo_files(repo_url): ...
def analyze_quality(files): ...
def summarize_with_llm(analysis): ...
```
---

### 3. Abstraction and Interfaces

The layer above does not care how the layer below works.
It only cares what it gets back.

```python
# Analysis layer calls this
def get_completion(prompt: str) -> str: ...

# Today: Gemini. Tomorrow: GPT-4.
# Analysis layer changes zero lines.
```
---

### 4. Design Patterns Used in RepoSense

**Facade Pattern  main.py**
One simple entry point that hides all internal complexity.
User runs one command. main.py coordinates all four layers internally.

**Strategy Pattern  gemini_client.py**
LLM provider is swappable. Gemini today, GPT tomorrow.
The calling layer never changes — only the strategy does.

**Template Method   prompt_builder.py**
Every prompt follows the same structure: Role + Context + Data + Output format.
Consistent structure = consistent, parsable LLM responses.

---

### 5. Context Windows and Chunking

LLMs can only read a fixed amount of text at once like RAM, not disk.

```
Without chunking:
200 files → send all → API error or garbage output

With chunking:
File (1000 lines)
    → Chunk 1 (lines 1–250)    → LLM → partial summary
    → Chunk 2 (lines 251–500)  → LLM → partial summary
    → Aggregate all summaries
```

RepoSense processes files individually, each file is one LLM call.
This is linear chunking, not full RAG.

---

### 6. RAG  Retrieval Augmented Generation

Instead of sending everything to the LLM, store content in a searchable
vector database and retrieve only relevant parts when needed.

```
All files → stored in vector DB
Query: "Where is authentication handled?"
    → Search vector DB
    → Retrieve top 5 relevant chunks
    → Send only those to LLM
    → Precise answer returned
```

RepoSense uses: Linear processing (no RAG yet)
---

### 7. Software Quality Metrics   ISO/IEC 25010

Measurable signals about code health. Numbers, not opinions.

| Metric | Measures | Tool |
|--------|----------|------|
| Cyclomatic Complexity | Decision paths in a function | radon |
| Coupling | External imports per file | count imports |
| Comment Density | Comments vs code ratio | count # lines |
| Maintainability Index | Overall maintainability 0–100 | radon |
| Lines of Code | File size | len(lines) |
| Test Detection | Presence of test files | check test_ prefix |

Key insight: High complexity = hard to test.
High coupling = hard to change. Low MI = high maintenance cost.

In RepoSense: Metrics are INPUT to LLM and LLM interprets numbers,
not guesses from raw code alone. This reduces hallucination.

---
### 8. Prompt Engineering as System Design

How you write the prompt determines quality, consistency,
and parsability of LLM output. It is an interface contract.

Three patterns used in RepoSense:

**Pattern 1  Role setting**
```
You are a senior software architect reviewing code for quality issues.
```

**Pattern 2  Factual grounding**
```
MEASURED QUALITY METRICS:
Complexity: 10.0
Coupling: 4 imports
Maintainability: 71.36
```

**Pattern 3  Structured output contract**
```
Return ONLY this JSON format:
{
  "purpose": "...",
  "patterns": [...],
  "quality_issues": [...],
  "severity": "low|medium|high",
  "recommendations": [...]
}
```
Combining all three = consistent, parsable, defensible output.
---
### 9. SDLC Model  Agile (Kanban)

RepoSense was developed using an Agile approach with Kanban-style
task flow — no fixed sprints, continuous layer-by-layer delivery.

| Agile Principle | How Applied |
|----------------|-------------|
| Working software over documentation | Each layer tested before next began |
| Responding to change | Model names, packages updated as deprecated |
| Continuous delivery | Daily commits to GitHub |
| Incremental builds | One layer per day, tested independently |

Phases were not strictly sequential — testing happened alongside
development, and requirements evolved as technical constraints emerged.


### 10. Software Development Techniques

**Preventive techniques   stop problems before they happen:**
- `.gitignore` — API key never reaches GitHub
- `timeout=10` on all requests — no infinite hangs
- `max_retries=5` — network failures handled gracefully
- `__init__.py` in every folder — Python module errors prevented
- `.env.example` — other developers know what keys are needed

**Adaptive techniques   respond to change:**
- Switched from `google-generativeai` to `google-genai` when deprecated
- Updated model from `gemini-1.5-flash` to `gemini-3.8-flash` when unavailable
- Reframed prompts when Gemini refused security-related content

**Maintenance techniques  keep code readable and changeable:**
- Docstrings on every function with Args, Returns, Raises
- Professional inline comments explaining why, not what
- Consistent naming conventions  snake_case functions, CAPS constants
- Single responsibility per file, easy to find and change things

**Corrective techniques  fix problems when they occur:**
- JSON parse error handling in `get_structured_response`
- Try/except around radon calls in `quality_analyzer`
- Retry logic with exponential-style wait for 503 errors
---

### 11. SDLC   Applied in RepoSense

| Phase | What We Did |
|-------|------------|
| Planning | Identified real pain — codebase comprehension takes hours |
| Requirements | Defined users — agencies, freelancers, tech leads |
| Design | Layered architecture, UML diagrams, folder structure |
| Implementation | Python, Gemini API, Radon, GitHub REST API |
| Testing | Unit tests per layer in tests/ folder |
| Deployment | GitHub with daily commits, open issues tracked |
| Maintenance | README, my-learning.md, future roadmap documented |

---
### 12. Context Engineering

Giving the LLM the right information in the right format
so it produces accurate, consistent responses.

In RepoSense prompt_builder.py:
- Role context → who the LLM is
- Data context → measured metrics as facts
- Output contract → strict JSON format enforced
- Task framing → what to look for and report

What we did NOT do yet:
- Few-shot examples (showing LLM example input/output pairs)
- Chain of thought (forcing step by step reasoning)
- Dynamic context (RAG — changing context per query)

---
### 13. Virtual Environments

Each project gets its own isolated environment.
Dependencies of one project never conflict with another.

```bash
python -m venv venv          # create
venv\Scripts\activate        # activate (Windows)
pip install package_name     # install into this env only
```

Always activate before running or installing anything.
Always add venv/ to .gitignore — never commit it.

---

### 14. Git Workflow   Daily Practice

```bash
git add .
git commit -m "day N: what was done"
git push
```

Commit message convention:
- day 1: project structure and LLM layer complete
- day 2: ingestion layer complete and tested
- day 3: analysis layer, prompt builder, UML diagrams

Never commit: .env, venv/, __pycache__/

---

## Errors and Bugs Log

| # | Error | Cause | Fix |
|---|-------|-------|-----|
| 1 | `venv/bin/activate` not found | Windows uses backslashes | `venv\Scripts\activate` |
| 2 | `mkdir` multiple folders failed | PowerShell limitation | Run mkdir one at a time |
| 3 | `init.py` not working | Missing double underscores | Must be `__init__.py` |
| 4 | `gemini-1.5-flash` error | Deprecated model | Use `gemini-3.8-flash` |
| 5 | `google-generativeai` warning | Deprecated package | Use `google-genai` |
| 6 | `response.txt` AttributeError | Typo | Use `response.text` |
| 7 | Indentation errors throughout | Manual typing | Always copy-paste code |
| 8 | `return` outside function | Code not indented inside def | Indent everything inside function |
| 9 | `content =_response` NameError | Typo with space | `content_response` |
| 10 | 503 UNAVAILABLE | Google server busy | Wait and retry |
| 11 | `RemoteDisconnected` error | Unstable internet | Reconnect and retry |
| 12 | `gemini-2.0-flash` not found | Outdated model name | Use `gemini-3.8-flash` |
| 13 | `ModuleNotFoundError: ingestion` | Running from wrong folder | Always run from project root |
| 14 | Git push rejected | Remote has newer commits | `git pull origin main --no-rebase` first |
| 15 | Gemini refused payload generation | Security content policy | Reframe as test cases, not attacks |

---
