---
name: modern-utility
description: >
  Compose small, fast CLI tools into Bash pipelines before reaching for a Python script. Use whenever searching or sizing a codebase, batch-replacing across files, or extracting, aggregating, and charting JSON/YAML, CSV/TSV, and logs.
---

# Modern Utility

Use fast CLI tools and shell pipelines as the first choice for search,
extraction, transformation, lightweight data analysis, and
visualization. When the work outgrows them, Python is the right
answer, not a defeat: the ordering exists so that simple work stays
simple, not to keep scripts out.

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
4. **Full Python script**: for multi-pass algorithms, stateful
   parsing, non-trivial joins, heavy libraries (`pandas`, `numpy`,
   ML), or charts past a quick terminal glance (`matplotlib`, or
   `plotly` when it should be interactive). Escalate here as soon as
   the task genuinely needs it — a pipeline contorted to avoid a
   script is harder to read, debug, and change than the script would
   have been.

## Preferred tools and fallbacks

Modern tools may not be installed. Check with `command -v` before
relying on one, then fall back:

| Task | Preferred | Fallback |
| :--- | :--- | :--- |
| Search / extract | `rg` | `grep -rE` (only if `rg` is missing) |
| Find files | `fd` | `find` |
| Lines of code by language | `tokei` | `scc` or `cloc`, else `fd -t f -e go -X wc -l` |
| Replace across files | `sd` | `perl -pi -e` or `sed -i` |
| JSON | `jq` | `python3 -c "import json, sys; ..."` |
| YAML | `yq` | `python3` + `yaml` |
| CSV / TSV | `qsv` or `mlr` | `awk` or `python3 -c "import csv; ..."` |
| SQL on CSV/JSON | `duckdb` | `sqlite3` or `python3` |
| Terminal charts | `uplot` (YouPlot) | plain-text summary (`sort \| uniq -c`) |

- `tokei` separates code from comments and blanks and honours
  `.gitignore`/`.ignore`, so its totals sit below a raw `wc -l`
  (`--no-ignore` and `--hidden` widen the scope back out). Narrow with
  `-t Go`, break it out per file with `-f`, order with `-s code`. Under
  `-o json`, `"Total"` is an entry beside the languages rather than a
  header — drop it before aggregating or every number doubles.
- `yq` means the Go implementation (https://github.com/mikefarah/yq),
  not the Python one — verify with `yq --version` (the Go build prints
  `mikefarah` in its version string).
- Python fallbacks for JSON/CSV use only the standard library, but
  YAML needs the third-party `yaml` (PyYAML) module — if both the CLI
  tool and the module are missing, report that instead of trying
  further workarounds.
- `uplot` reads TSV by default (`-d` for other delimiters, `-H` for a
  header row) and draws the chart on **stderr**, leaving stdout free
  for the data itself. It answers "what does this look like" at a
  glance; multiple series, annotations, controlled scales, or a saved
  image file call for a full Python script — reach for `matplotlib`
  rather than fighting a terminal plot.
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
- **Codebase size at a glance** (bare `tokei` walks the current
  directory; the second form is the per-file breakdown for one
  language):
  ```bash
  tokei
  tokei -t Python -f -s code
  ```
- **Language mix as a chart**:
  ```bash
  tokei -o json | jq -r 'to_entries | map(select(.key != "Total")) | sort_by(-.value.code)[] | "\(.key)\t\(.value.code)"' | uplot bar -t 'Code lines'
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
- **Terminal chart straight from a pipeline** (`uplot count` counts
  occurrences itself — no `sort | uniq -c` needed):
  ```bash
  rg -oN --no-filename 'ERROR \[\w+\]' server.log | uplot count -t 'Errors'
  ```
- **Histogram of a numeric column**:
  ```bash
  qsv select response_ms data.csv | tail -n +2 | uplot hist --nbins 20
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
- Prefer pipelines or `python3 -c` over leaving one-off script files
  behind in the workspace — but when a task genuinely calls for a
  script, write a real one instead of cramming it into `-c`.
