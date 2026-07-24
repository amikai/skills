---
name: modern-utility
description: >
  Prefer fast, modern CLI tools (Rust/Go/C) and Bash pipelines over Python scripts for daily tasks and lightweight data analysis. Use whenever searching codebases, performing batch file replacements, parsing JSON/YAML, or analyzing CSV/TSV/logs.
---

# Modern Utility

Use fast CLI tools and shell pipelines as the first choice for search,
extraction, transformation, and lightweight data analysis. Use Python
only as glue when a pipeline becomes unreadable, and a full Python
script only when the task genuinely needs one.

## Hierarchy

1. **Agent built-in tools**: for single-step work — searching, reading
   files, small edits. Small targeted edits should go through the
   agent's edit tool so changes stay reviewable, not through `sed`/`sd`.
2. **CLI pipeline in the shell**: when the work needs chaining (`|`) —
   extracting regex capture groups, filter + aggregate, feeding matches
   into downstream tools in one step without flooding context. In
   pipelines, search with `rg` (e.g. `rg -o`, `rg -N --no-filename`),
   not `grep` and not the agent's built-in search tool.
3. **Inline Python glue (`python3 -c "..."`)**: when string logic or
   nested-structure handling gets awkward in pure shell.
4. **Full Python script**: only for multi-pass algorithms or heavy
   libraries (`pandas`, `numpy`, ML).

## Preferred tools and fallbacks

Modern tools may not be installed. Check with `command -v` before
relying on one, then fall back:

| Task | Preferred | Fallback |
| :--- | :--- | :--- |
| Search / extract | `rg` | `grep -rE` (only if `rg` is missing) |
| Find files | `fd` | `find` |
| Replace across files | `sd` | `perl -pi -e` or `sed -i` |
| JSON | `jq` | `python3 -c "import json, sys; ..."` |
| YAML | `yq` | `python3` + `yaml` |
| CSV / TSV | `qsv` or `mlr` | `awk` or `python3 -c "import csv; ..."` |
| SQL on CSV/JSON | `duckdb` | `sqlite3` or `python3` |

- `yq` means the Go implementation (https://github.com/mikefarah/yq),
  not the Python one — verify with `yq --version` (the Go build prints
  `mikefarah` in its version string).
- Python fallbacks for JSON/CSV use only the standard library, but
  YAML needs the third-party `yaml` (PyYAML) module — if both the CLI
  tool and the module are missing, report that instead of trying
  further workarounds.
- Check availability with an explicit `if`, not an `&& … ||` chain
  (a chain falls through to the fallback when the tool exists but the
  query fails, hiding the real error):

  ```bash
  if command -v yq >/dev/null 2>&1; then
    yq '.version' config.yaml
  else
    python3 -c 'import yaml; print(yaml.safe_load(open("config.yaml"))["version"])'
  fi
  ```

## Recipes

- **Frequency count from logs**:
  ```bash
  rg -o 'ERROR \[\w+\]' server.log | sort | uniq -c | sort -rn | head -n 10
  ```
- **Batch replace** (bulk mechanical renames only; use the agent's edit
  tool for a handful of edits):
  ```bash
  fd -t f -e ts -e js -X sd 'v1/api' 'v2/api'
  ```
- **YAML read / in-place edit**:
  ```bash
  yq '.metadata.name' deployment.yaml
  yq -i '.spec.replicas = 3' deployment.yaml
  ```
- **CSV summary stats** (`--cache-threshold 0` avoids sidecar cache files):
  ```bash
  qsv stats --cache-threshold 0 --everything data.csv | head -n 30
  ```
- **SQL directly on a file**:
  ```bash
  duckdb -c "SELECT status_code, COUNT(*) AS cnt FROM 'access.log.csv' GROUP BY status_code ORDER BY cnt DESC"
  ```
- **Python glue on CLI output**:
  ```bash
  jq -c '.items[]' data.json | python3 -c '
  import sys, json
  for line in sys.stdin:
      item = json.loads(line)
      print(item["id"], item["score"] * 100)
  '
  ```

## Rules

- Cap long outputs (`… | head -n 50`, `qsv slice -l 50`) to avoid
  flooding context. Note `rg -m 50` limits matches per file, not
  globally — pipe through `head` for a global cap.
- Prefer pipelines or `python3 -c` over writing one-off script files
  into the workspace.
