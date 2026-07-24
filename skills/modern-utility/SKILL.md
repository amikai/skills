---
name: modern-utility
description: >
  Compose fast CLI tools into Bash pipelines for search, batch edit, data analysis, and log processing before escalating to Python.
---

# Modern Utility

Compose fast CLI tools and shell pipelines for code search, extraction, data analysis, and visualization before escalating to Python scripts.

## Workflow

1. **Select tier**:
   - Tier 1: Agent built-in tools for single-file operations.
   - Tier 2: Shell pipelines (`|`) for regex extraction, filtering, or aggregations without context flooding.
   - Tier 3: Inline Python (`python3 -c "..."`) when string manipulation or JSON parsing becomes awkward in pure shell.
   - Tier 4: Escalate to full Python script for multi-pass logic, heavy libraries (`pandas`, `matplotlib`), or complex stateful parsing.
2. **Verify availability**: Test optional tools using explicit `if command -v tool >/dev/null 2>&1; then` checks before invocation.
3. **Compose & cap**: Build pipelines and cap terminal output (`| head -n 50`) to avoid flooding context.

*Completion Criterion*: Pipeline returns exact query results without context flooding (≤50 lines), uses standard fallbacks when modern CLI tools are absent, and leaves no temporary script sediment.

## Tool Selection & Fallbacks

| Task | Preferred | Fallback |
| :--- | :--- | :--- |
| Search / extract | `rg` | `grep -rE` |
| Find files | `fd` | `find` |
| Lines of code | `tokei` | `scc` / `cloc`, or `fd -t f -e go -X wc -l` |
| Replace across files | `sd` | `perl -pi -e` / `sed -i` |
| JSON | `jq` | `python3 -c "import json, sys; ..."` |
| YAML | `yq` | `python3` + `yaml` |
| CSV / TSV | `qsv` / `mlr` | `awk` / `python3 -c "import csv, sys; ..."` |
| SQL on CSV/JSON | `duckdb` | `sqlite3` / `python3` |
| Terminal charts | `uplot` (YouPlot) | Plain-text summary (`sort \| uniq -c`) |

## Tool Rules

- **`tokei`**: Use `code` line count to exclude comments/blanks. In JSON mode (`-o json`), filter out `"Total"` to avoid doubled sums.
- **`yq`**: Requires Go build (`mikefarah/yq`). Verify version (`yq --version`).
- **`uplot`**: Expects TSV input by default; outputs charts to `stderr` to preserve stdout piping.
- **Safe tool check pattern**:

  ```bash
  if command -v yq >/dev/null 2>&1; then
    yq '.version' config.yaml
  else
    python3 -c 'import yaml; print(yaml.safe_load(open("config.yaml"))["version"])'
  fi
  ```

## Recipes

- **Log frequency count**:
  ```bash
  rg -o 'ERROR \[\w+\]' server.log | sort | uniq -c | sort -rn | head -n 10
  ```
- **Batch replace across files**:
  ```bash
  fd -t f -e ts -e js -X sd 'v1/api' 'v2/api'
  ```
- **Codebase size summary**:
  ```bash
  tokei -t Python -f -s code
  ```
- **Language distribution chart**:
  ```bash
  tokei -o json | jq -r 'to_entries | map(select(.key != "Total")) | sort_by(-.value.code)[] | "\(.key)\t\(.value.code)"' | uplot bar -t 'Code lines'
  ```
- **YAML in-place edit**:
  ```bash
  yq -i '.spec.replicas = 3' deployment.yaml
  ```
- **CSV summary stats**:
  ```bash
  qsv stats --cache-threshold 0 --everything data.csv | head -n 30
  ```
- **SQL on file**:
  ```bash
  duckdb -c "SELECT status_code, COUNT(*) AS cnt FROM 'access.log.csv' GROUP BY status_code ORDER BY cnt DESC"
  ```
- **Inline Python glue**:
  ```bash
  jq -c '.items[]' data.json | python3 -c '
  import sys, json
  for line in sys.stdin:
      item = json.loads(line)
      print(item["id"], item["score"] * 100)
  '
  ```

## Execution Guardrails

- **Output capping**: Always cap pipeline output (`| head -n 50` or `qsv slice -l 50`).
- **No temporary script sediment**: Use inline Python (`python3 -c`) or pipelines. Do not write temporary `.py` files to the codebase unless escalation to a formal script is required.
