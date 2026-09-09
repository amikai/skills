---
name: modern-utility
description: >
  Use when choosing CLI tools for search, codebase sizing, batch text replacement,
  or extracting, aggregating, and charting JSON/YAML, CSV/TSV, and logs.
---

# Preferred CLI tools (Bash)

Prefer the tools below when they fit the task, including inside pipes (`| rg foo`, not `| grep foo`). Use classic tools when their capabilities or output better suit the task.

If a preferred tool is unavailable, use a suitable alternative without commentary. Do not hide execution errors.

- Prefer `rg` to `grep` for searching file contents, filtering text streams, and extracting matches, including inside pipelines.
- Prefer `fd` to `find` for locating files and directories by name, extension, or path, and passing selections to other commands.
- Use `tokei` to measure codebase size, with breakdowns of code, comments, and blank lines by language or file.
- Use `sd` for literal or regex text replacement, including consistent replacements across multiple files.
- Use `jq` to query, filter, transform, and aggregate JSON, or format results for other commands.
- Use `yq` (mikefarah/yq) to query, update, merge, and transform YAML, including multi-document files and conversion between supported formats.
- Use `qsv` / `mlr` for tabular data processing such as selecting columns, filtering rows, sorting, joining, and computing summaries over CSV/TSV.
- Use `duckdb` for SQL-based data exploration, joins, aggregation, window functions, and data conversion across tables and files such as CSV, JSON, and Parquet.
- Use `uplot` (YouPlot) to visualize data in the terminal with charts such as bars, histograms, line plots, and scatter plots.

## Working principles

- Use the agent's read/edit tools for simple file operations and small edits; preview batch replacements and review the resulting diff.
- Prefer CLI pipelines over ad-hoc scripts when they stay readable. Use Python or another suitable runtime when the logic warrants it.
- Run temporary or standalone Python scripts with `uv run script.py` rather than invoking system `python3` directly. Declare dependencies in PEP 723 inline script metadata so others can run the file without extra flags.
- Use parsers that understand the input format, and keep output focused to avoid flooding context.
