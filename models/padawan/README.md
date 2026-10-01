# Padawan

An LLM-prompted assistant that generates `pytest-bdd` feature files and step definitions from
Python source modules.

## Why a prompted wrapper, not a fine-tuned model

This is the repo's first model and is expected to grow into a product, so the first version is
deliberately the cheapest one that can prove demand: a thin wrapper around Claude, not a
fine-tuning pipeline. Fine-tuning needs a curated dataset of good pytest-bdd examples that doesn't
exist yet; a prompted wrapper needs none, ships now, and is directly useful for collecting that
dataset from real usage later. If usage validates the idea, the natural next step is a fine-tuned
or retrieval-augmented successor trained on accepted generations — at that point this version's
`LLMClient` port (see `core/generator.py`) lets the Anthropic adapter be swapped out without
touching the generation logic.

## Architecture

- `core/` — pure logic, no I/O. `prompts.py` builds the generation prompt; `generator.py`
  orchestrates prompt construction and delegates to an `LLMClient` port.
- `adapters/` — concrete integrations. `llm_client.py` implements `LLMClient` against the
  Anthropic API.
- `config.py` — `Settings`, loaded from the environment (`pydantic-settings`).
- `cli.py` — the `padawan` command-line entrypoint (`click`).

## Usage

```bash
export ANTHROPIC_API_KEY=sk-...
uv run python -m models.padawan.cli generate --source path/to/module.py
uv run python -m models.padawan.cli generate --source path/to/module.py --out tests/module.feature
```

## Configuration

| Variable             | Required | Default            | Description                          |
|-----------------------|----------|---------------------|---------------------------------------|
| `ANTHROPIC_API_KEY`  | yes      | —                   | Anthropic API key.                    |
| `MODEL`              | no       | `claude-sonnet-5`   | Claude model used for generation.     |
| `MAX_TOKENS`         | no       | `4096`              | Max tokens requested per generation.  |

## Not built yet (by design)

- **Eval harness.** The highest-value next step is running generated tests against the target
  module's own test suite and reporting pass/fail — an objective signal this repo doesn't have
  for any other model type. Deferred until there's a second real use case to validate the shape
  against.
- **Retrieval of few-shot examples.** Worth adding once there's a corpus of accepted generations
  to draw from; none exists yet.
