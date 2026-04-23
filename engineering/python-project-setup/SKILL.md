---
name: python-project-setup
description: Use when initializing a new Python project, setting up a development environment, or migrating from legacy tools (pip, venv, pyenv, Black, isort, Flake8, mypy, Poetry, pandas). Also triggers for questions about uv, Ruff, Ty, Polars, or pyproject.toml configuration in 2026.
---

# Python Project Setup: The Astral-Polars Stack

## Overview

The 2026 Python stack unifies environment management, code quality, and data processing into four tools under a single `pyproject.toml`. Three of the four tools (uv, Ruff, Ty) are developed by Astral.

| Function | 2026 Tool | Replaces |
|----------|-----------|---------|
| Environment & packages | **uv** | pip, venv, pyenv, Poetry, conda |
| Linting & formatting | **Ruff** | Black, isort, Flake8 |
| Type checking | **Ty** | mypy, Pyright |
| Data manipulation | **Polars** | pandas |

## When NOT to Use

Evaluate before migrating if:
- Team has a mature, functioning Poetry or mypy workflow
- Codebase depends on pandas-only ecosystem libraries
- Organization has standardized on Pyright
- Legacy repo where migration friction outweighs performance gains

---

## Quick Setup

```bash
# 1. Install uv (once per machine — no Python or Rust required)
curl -LsSf https://astral.sh/uv/install.sh | sh  # macOS/Linux
# powershell -c "irm https://astral.sh/uv/install.ps1 | iex"  # Windows

# 2. Scaffold project with src/ layout
uv init my-project && cd my-project
mkdir -p src/my_project tests
mv hello.py src/my_project/__init__.py

# 3. Pin Python version (writes .python-version for team consistency)
uv python pin 3.12

# 4. Add dev tools and sync
uv add --dev ruff ty
uv sync
```

---

## pyproject.toml Template

```toml
[project]
name = "my-project"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = []

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/my_project"]

[dependency-groups]
dev = ["ruff>=0.9", "ty>=0.0.1a1"]

[tool.ruff]
line-length = 100
src = ["src"]

[tool.ruff.lint]
# E/F = pycodestyle/pyflakes, B = bugbear, I = isort, UP = pyupgrade
select = ["E", "F", "B", "I", "UP"]

[tool.ruff.lint.isort]
known-first-party = ["my_project"]

[tool.ty]
python-version = "3.12"
exclude = ["data/", "notebooks/"]
```

---

## Daily Commands

| Task | Command |
|------|---------|
| Run script | `uv run python src/my_project/main.py` |
| Add dependency | `uv add requests` |
| Add dev dependency | `uv add --dev pytest` |
| Lint with auto-fix | `uv run ruff check --fix .` |
| Format | `uv run ruff format .` |
| Type check | `uv run ty check src/` |
| Run one-off tool | `uvx ruff --version` (no permanent install) |
| CI install (exact lockfile) | `uv sync --frozen` |

**Key insight:** `uv run` handles virtual environment activation automatically — never `source .venv/bin/activate`.

---

## Adding Polars

```bash
uv add polars
# For large file workflows:
uv add polars pyarrow
```

### Lazy Execution (Core Pattern)

```python
import polars as pl

# ❌ Eager — loads entire file, then filters
df = pl.read_csv("data.csv").filter(pl.col("region") == "US")

# ✅ Lazy — optimizer pushes filter down, skips unused columns
df = (
    pl.scan_csv("data.csv")               # scan_parquet() for Parquet files
    .filter(pl.col("region") == "US")
    .select(["id", "region", "revenue"])
    .collect()
)
```

### Expressions over UDFs

```python
# ❌ Row-wise UDF — slow, single-threaded
df.with_columns(pl.col("price").map_elements(lambda x: x * 1.1))

# ✅ Native expression — vectorized, parallelized
df.with_columns((pl.col("price") * 1.1).alias("price_with_tax"))
```

**File format preference:** Parquet over CSV for internal data. Use CSV only at ingestion boundary.

---

## Version Control & CI

```bash
# Always commit the lockfile
git add uv.lock

# CI: install from exact lockfile (fast, reproducible)
uv sync --frozen
```

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Using `mypy` ("most mature") | Use `Ty` — it's the 2026 standard; mypy is legacy |
| Including `pandas` "for ecosystem compatibility" | Use Polars only; reach for pandas only if a specific library requires it |
| Line length 88 (Black default) | Set `line-length = 100` in `[tool.ruff]` |
| `pip install` in the project | `uv add <package>` keeps lockfile in sync |
| `source .venv/bin/activate` | Use `uv run <cmd>` — no activation needed |
| Pandas-style `.map_elements()` UDF in Polars | Use native Polars expressions |
| `pl.read_csv()` on large files | `pl.scan_csv().collect()` for lazy loading |
| CI without `--frozen` | `uv sync --frozen` for reproducible builds |
| `.gitignore`-ing `uv.lock` | Commit it — it ensures cross-machine consistency |
| Installing Ruff/Ty globally | Add with `--dev` flag; scoped to the project |
