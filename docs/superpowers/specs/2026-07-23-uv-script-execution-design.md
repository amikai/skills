# uv Script Execution Design

**Date:** 2026-07-23
**Status:** Approved

## Problem

`scripts/gen_catalog.py` and `scripts/bump.py` sometimes fail to run:
they lack the executable bit, and they depend on a system `python3`
being on PATH with a compatible version.

## Design

Make both scripts self-contained uv scripts, and make uv the single
documented way to run them.

1. **Shebang + PEP 723 metadata** in both scripts:

   ```python
   #!/usr/bin/env -S uv run --script
   # /// script
   # requires-python = ">=3.10"
   # dependencies = []
   # ///
   ```

   uv resolves (and downloads if needed) a matching Python, so the
   scripts no longer depend on the system `python3`. Both scripts are
   stdlib-only, hence empty dependencies.

2. **`chmod +x`** on both scripts so `./scripts/xxx.py` works directly.

3. **Callers updated**: `.github/workflows/ci.yml` and `README.md`
   invoke `uv run scripts/xxx.py` instead of `python3 scripts/xxx.py`.
   CI installs uv via `astral-sh/setup-uv` (the runner image does not
   ship it). The generic `python3 -m json.tool` manifest check in CI
   is out of scope and unchanged.

## Verification

- `uv run scripts/gen_catalog.py --check` and
  `uv run scripts/bump.py --check` pass locally.
- `./scripts/gen_catalog.py --check` runs directly (shebang + exec bit).
- CI stays green.
