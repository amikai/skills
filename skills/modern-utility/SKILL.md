---
name: modern-utility
description: >
  Prefer fast, modern CLI tools (Rust/Go/C) and Bash pipelines over Python scripts for daily tasks and lightweight data analysis.
---

# Modern Utility (Speed-Optimized for Coding Agents)

This skill mandates using ultra-fast CLI tools (Rust/Go/C) and single-line Bash pipelines as the primary choice for search, extraction, transformation, and lightweight data analysis tasks. Python serves as a secondary glue script or last resort when CLI pipelines alone become unreadable or inadequate.

## Native Agent Tools vs. CLI Pipelines

- **Native Agent Tools (`grep_search`, `view_file`, `list_dir`)**: Use native tools for simple single-step code searches or direct file viewing.
- **CLI Tools in Pipelines (`rg`, `fd`, `sd` via `run_command`)**: Use CLI tools when **chaining within Bash pipelines (`|`)**. Use `rg` to extract regex capture groups (`rg -o`), filter logs, or feed matching lines directly into downstream tools (`awk`, `sd`, `jaq`, `yq`, `sort`, `uniq`, `python -c`) in a single step without flooding the LLM context.

## Core Hierarchy & Execution Strategy

1. **CLI & Bash Pipeline (Primary)**: Use fast CLI tools (`rg`, `fd`, `sd`, `jaq`, `yq`, `qsv`, `duckdb`, `awk`) directly in shell pipelines (`|`). This delivers sub-10ms execution and zero workspace file pollution.
2. **Python as Glue / Secondary Helper (`python -c`)**: When interacting with CLI output or when complex string transformation/regex parsing is awkward in pure Bash, use lightweight inline Python commands (`python -c "..."`) or quick glue scripts to combine CLI inputs and outputs.
3. **Heavy Python Scripts (Last Resort)**: Reserve full Python scripts and heavy libraries (e.g., `pandas`, `scipy`) for tasks requiring complex multi-pass algorithms, machine learning models, or heavy matrix operations.

## Tool Selection & Fallback Hierarchy

- **Tier 1: Modern Rust / Go / C CLI (Primary Choice)**
  - Tools: `rg`, `fd`, `sd`, `jaq`, `yq`, `qsv`, `duckdb`, `mlr`, `awk`
  - Use for: Pipeline-based text extraction (`rg`), file discovery (`fd`), pattern replacement (`sd`), JSON querying (`jaq`), YAML/TOML querying and editing (`yq`), CSV/TSV processing (`qsv`), and in-memory SQL analytics (`duckdb`).
- **Tier 2: Python as Glue / Inline Helper (`python -c "..."`)**
  - Trigger: When complex string logic, regex manipulation, or nested JSON parsing becomes awkward in pure Bash pipelines.
  - Use for: Formatting CLI output, transforming JSON objects, or gluing inputs/outputs between CLI commands.
- **Tier 3: Dedicated Python Script / Heavy Frameworks**
  - Trigger: When heavy third-party libraries or multi-stage algorithms are strictly required.
  - Use for: `pandas`, `numpy`, machine learning models, complex multi-step data pipelines, or heavy mathematical operations.

> **Pro Tip**: Check tool availability before assuming installation:
> ```bash
> command -v yq >/dev/null 2>&1 && yq '.version' config.yaml || python -c "import yaml..."
> ```

## Agent Speed Matrix (Task → Primary CLI vs Secondary Python)

| Agent Task | Primary CLI Command (Piped in `run_command`) | Secondary Python Glue (`python -c`) |
| :--- | :--- | :--- |
| **Pipeline Search & Extract** | `rg -o 'error:\s*\w+' log/ \| sort \| uniq -c` | `python -c "import sys, re; ..."` |
| **Find Files & Pipe** | `sd 'old' 'new' $(fd -e ts)` | `python -c "import pathlib; ..."` |
| **JSON Key Extraction** | `jaq -r '.key' file.json \| sort` | `python -c "import json, sys; ..."` |
| **YAML / TOML Key Extract & Edit** | `yq '.services.web.image' docker-compose.yml` | `python -c "import yaml, sys; ..."` |
| **CSV/TSV Filtering** | `qsv select col1,col2 data.csv \| head -n 30` | `python -c "import csv, sys; ..."` |
| **SQL on CSV/TSV/JSON** | `duckdb -c "SELECT ... FROM 'data.csv'"` | `python -c "import sqlite3..."` or `pandas` |

## Command Patterns & Python Glue Recipes

### 1. Codebase & File Operations
* **Pipeline Regex Search & Extraction**:
  ```bash
  rg -o 'ERROR \[\w+\]' server.log | sort | uniq -c | sort -rn
  ```
* **Batch String Replacement**:
  ```bash
  sd 'v1/api' 'v2/api' $(fd -e ts -e js)
  ```
* **YAML Field Extraction & In-Place Editing**:
  ```bash
  # Extract key
  yq '.metadata.name' deployment.yaml
  # Update field in-place
  yq -i '.spec.replicas = 3' deployment.yaml
  ```

### 2. Tabular Data & Log Analysis
* **Inspect CSV/TSV Summary Statistics**:
  ```bash
  qsv stats --everything data.tsv | head -n 30
  ```
* **SQL Query directly on Log/CSV**:
  ```bash
  duckdb -c "SELECT status_code, COUNT(*) AS cnt FROM 'access.log.csv' GROUP BY status_code ORDER BY cnt DESC;"
  ```
* **Python Glue Example (using `python -c` with CLI output)**:
  ```bash
  # Extract JSON with jaq, then format or transform using python inline
  jaq -c '.items[]' data.json | python -c "import sys, json; [print(j['id'], j['score']*100) for j in (json.loads(line) for line in sys.stdin)]"
  ```

### 3. Frequency & Truncation
* **Top 10 Most Frequent Values**:
  ```bash
  qsv frequency -s category data.csv -l 10
  # Fallback using Unix pipeline:
  cut -d',' -f2 data.csv | sort | uniq -c | sort -rn | head -n 10
  ```

## Practical Guidelines for Agents

- ✅ **Native Tools vs. CLI Pipeline**: Use native tools (`grep_search`, `view_file`) for standard inspection. Use `rg` inside Bash pipelines (`run_command`) when filtering, extracting regex capture groups (`rg -o`), or piping search results directly into downstream tools.
- ✅ **Prefer CLI + Pipelines**: Start with CLI tools for maximum speed and sub-10ms response.
- ✅ **Use Python as Glue**: Feel free to use `python -c "..."` or a small Python snippet to process, format, or glue CLI outputs when Bash syntax becomes overly cryptic.
- ❌ **Limit Output Size**: Always cap long outputs with `head -n 50`, `qsv slice -l 50`, or `rg -m 50` to avoid flooding tool output and wasting context tokens.
