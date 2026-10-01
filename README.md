# models

Shared home for AI/ML models developed under the `jedi-knights` org. The goal is to avoid
re-solving data loading, training loops, evaluation, logging, and config management for every
new model — that infrastructure lives once, in `common/`, and each model is a thin, isolated
consumer of it.

## Repo layout

- `common/` — shared library code: data loading, training utilities, evaluation metrics,
  logging, and config helpers. If two or more models need the same piece of infrastructure, it
  belongs here.
- `models/` — one subdirectory per model, e.g. `models/<model_name>/`. Each model owns its own
  entrypoint, config, and README, and reuses `common/` wherever possible.
- `experiments/` — scratch space for one-off scripts and research notebooks that aren't ready to
  live as a real model yet.
- `configs/` — shared or model-specific YAML config files.
- `scripts/` — utility scripts: setup, data download, repo maintenance.
- `tests/` — tests for `common/` and other shared tooling.

## Setup

This project uses [`uv`](https://docs.astral.sh/uv/) for dependency and virtual environment
management, targeting Python 3.12.

```bash
uv sync
source .venv/bin/activate
```

Run the test suite and linter:

```bash
uv run pytest
uv run ruff check .
uv run mypy common/
```

## Adding a new model

1. Create `models/<model_name>/` with its own `README.md`, config, and entrypoint script.
2. Reuse `common/` for data loading, training loops, evaluation, logging, and config parsing
   wherever it fits — extend `common/` rather than duplicating logic inside the model directory.
3. Only break a model out into its own repo if it needs an incompatible dependency stack (e.g. a
   conflicting framework version) or an independent release cycle. Until then, keep it here —
   the mono-repo is what makes sharing `common/` cheap.
