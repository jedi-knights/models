# Contributing

## Branch naming

- `feature/<short-description>` for new functionality (a new model, a new shared utility).
- `fix/<short-description>` for bug fixes.

## Before pushing

Run the full local check locally — it mirrors CI:

```bash
uv run ruff check .
uv run mypy common/
uv run pytest
```

All three must pass before opening a PR.

## Code style

- Formatting and linting are enforced by `ruff`; run `uv run ruff check .` (and `uv run ruff
  format .` if you want auto-formatting) before committing.
- Type hints are expected on all code in `common/`, since it's shared infrastructure consumed by
  every model. `mypy common/` runs in strict mode.
- Code under `models/<model_name>/` and `experiments/` can be looser — research code iterates
  fast — but anything promoted into `common/` must be typed and tested.
