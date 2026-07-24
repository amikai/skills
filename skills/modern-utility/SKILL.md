---
name: modern-utility
description: >
  Compose fast CLI tools into Bash pipelines before writing Python scripts. Use for search, codebase sizing, batch replacement, and extracting, aggregating, or charting JSON/YAML, CSV/TSV, and logs.
---

# Modern Utility

Use fast CLI tools and shell pipelines as the primary choice for search, extraction, transformation, data analysis, and visualization. Upgrade to Python when task complexity warrants it.

## Hierarchy

1. **Agent built-in tools**: For single-step tasks (search, read, edit). Use the edit tool for small edits to keep changes reviewable (avoid `sed`/`sd`).
2. **CLI shell pipelines**: For chained operations (`|`) like regex capture or filter-aggregate without flooding context. Use `rg` (e.g. `rg -o`, `rg -N --no-filename`) in pipelines instead of `grep` or built-in search.
3. **Inline Python (`python3 -c "..."`)**: When string logic or nested structures become awkward in pure shell.
4. **Full Python script**: For multi-pass algorithms, stateful parsing, complex joins, heavy libraries (`pandas`, `numpy`), or non-terminal plots (`matplotlib`, `plotly`). Escalate early if a pipeline becomes unreadable.

## Preferred Tools and Fallbacks

Check availability with `command -v` before using modern tools:

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

### Tool Notes

- **`tokei`**: Excludes comments/blanks and respects `.gitignore`/`.ignore` (use `--no-ignore` / `--hidden` to widen). Key flags: `-t <Lang>`, `-f` (per-file breakdown), `-s code` (sort by code). In JSON mode (`-o json`), filter out the `"Total"` entry to avoid doubling aggregate sums.
- **`yq`**: Must be the Go build (github.com/mikefarah/yq). Verify with `yq --version` (contains `mikefarah`).
- **Python fallbacks**: JSON/CSV use stdlib. YAML requires PyYAML (`import yaml`). If both CLI tool and `yaml` module are missing, report unavailability rather than attempting further workarounds.
- **`uplot`**: Expects TSV by default (`-d` for delimiter, `-H` for headers) and outputs charts to **stderr** (preserving clean stdout data). Escalate to `matplotlib` for multi-series, annotations, or image exports.
- **Tool Check Syntax**: Use explicit `if` statements instead of `&& ... ||` chains to prevent swallowing query errors:

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
- **Batch replace** (use agent edit tool for small edits):
  ```bash
  fd -t f -e ts -e js -X sd 'v1/api' 'v2/api'
  ```
- **Codebase size**:
  ```bash
  tokei
  tokei -t Python -f -s code
  ```
- **Language mix chart**:
  ```bash
  tokei -o json | jq -r 'to_entries | map(select(.key != "Total")) | sort_by(-.value.code)[] | "\(.key)\t\(.value.code)"' | uplot bar -t 'Code lines'
  ```
- **YAML read / in-place edit**:
  ```bash
  yq '.metadata.name' deployment.yaml
  yq -i '.spec.replicas = 3' deployment.yaml
  ```
- **CSV summary stats** (`--cache-threshold 0` disables sidecar files):
  ```bash
  qsv stats --cache-threshold 0 --everything data.csv | head -n 30
  ```
- **SQL directly on a file**:
  ```bash
  duckdb -c "SELECT status_code, COUNT(*) AS cnt FROM 'access.log.csv' GROUP BY status_code ORDER BY cnt DESC"
  ```
- **Pipeline chart** (`uplot count` aggregates directly):
  ```bash
  rg -oN --no-filename 'ERROR \[\w+\]' server.log | uplot count -t 'Errors'
  ```
- **Histogram**:
  ```bash
  qsv select response_ms data.csv | tail -n +2 | uplot hist --nbins 20
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

## Rules

- **Cap output**: Use `| head -n 50` or `qsv slice -l 50` to avoid context flooding. (`rg -m 50` limits per-file matches, not globally; pipe to `head` for global capping).
- **Avoid leftover scripts**: Prefer pipelines or `python3 -c` over leaving temporary `.py` files. Create formal script files only when logic complexity truly requires it.

