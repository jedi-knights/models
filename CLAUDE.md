# models

Mono-repo for AI/ML model development under the `jedi-knights` org. Early-stage research repo —
favor simplicity and clarity over premature abstraction. Don't build infrastructure in `common/`
speculatively; only extract shared code once a second model actually needs it.

## Layout and conventions

- `common/` — shared infrastructure only (data loading, training loops, eval metrics, logging,
  config helpers). Typed, tested, reviewed like a library — other models depend on it.
- `models/<model_name>/` — one directory per model. Each has its own README, config, and
  entrypoint. Model-specific code stays here, not in `common/`.
- `experiments/` — scratch scripts and notebooks that haven't earned a place under `models/` yet.
- `configs/` — YAML configs, shared or per-model.
- `scripts/` — setup/maintenance utilities, not model code.
- `tests/` — covers `common/` and shared tooling, not individual models (each model can carry its
  own tests under its own directory if needed).

## Adding a new model

Create `models/<model_name>/` with its own README, config, and entrypoint script. Reuse
`common/` wherever possible rather than re-implementing data loading, training, eval, or logging
inside the model directory. Only split a model into its own repo when it needs an incompatible
dependency stack or an independent release cycle — until then, keeping it here is what makes
sharing `common/` cheap.

## Tooling

- `uv` for dependency/venv management, Python 3.12.
- `ruff` for lint, `mypy common/` for type checking (strict), `pytest` for tests.
- CI (`.github/workflows/ci.yml`) runs all three on push/PR to `main`.
