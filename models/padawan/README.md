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

- `core/` — pure logic, no I/O.
  - `prompts.py` builds the generation prompt, requesting a fenced ` ```gherkin ` block and a
    fenced ` ```python ` block so the output can be parsed back apart.
  - `generator.py` orchestrates prompt construction and delegates to an `LLMClient` port.
  - `parser.py` splits raw LLM output into a `GeneratedTests(feature, steps)` pair.
  - `evaluator.py` stages `GeneratedTests` next to the original source and delegates to a
    `TestRunner` port to actually run them.
- `adapters/` — concrete integrations.
  - `llm_client.py` implements `LLMClient` against the Anthropic API.
  - `pytest_runner.py` implements `TestRunner` by running `pytest` in a bounded subprocess.
- `config.py` — `Settings`, loaded from the environment (`pydantic-settings`).
- `cli.py` — the `padawan` command-line entrypoint (`click`): `generate` and `eval`.

## Usage

```bash
export ANTHROPIC_API_KEY=sk-...

# Print generated pytest-bdd output (a ```gherkin block + a ```python block) to stdout
uv run python -m models.padawan.cli generate --source path/to/module.py

# Write it to a file instead
uv run python -m models.padawan.cli generate --source path/to/module.py --out out.txt

# Generate AND run the result against the real module, reporting pytest's pass/fail summary.
# Exits non-zero if the generated suite fails.
uv run python -m models.padawan.cli eval --source path/to/module.py
```

`eval` is the objective quality signal this repo doesn't have for any other model type: it
doesn't just produce text, it runs the text and tells you whether the generation was actually
correct. `models/padawan/tests/test_eval_integration.py` exercises the real staging →
pytest-bdd discovery → subprocess path (with a hand-written generation, not a live LLM call) so
that path is covered by something other than mocks.

## Configuration

| Variable             | Required | Default            | Description                          |
|-----------------------|----------|---------------------|---------------------------------------|
| `ANTHROPIC_API_KEY`  | yes      | —                   | Anthropic API key.                    |
| `MODEL`              | no       | `claude-sonnet-5`   | Claude model used for generation.     |
| `MAX_TOKENS`         | no       | `4096`              | Max tokens requested per generation.  |

## Not built yet (by design)

- **Retrieval of few-shot examples.** Worth adding once there's a corpus of accepted generations
  to draw from; none exists yet.
- **Dataset collection from eval results.** `eval`'s pass/fail signal is exactly what a future
  fine-tuned or retrieval-augmented successor would train on — but persisting results anywhere is
  deferred until there's real usage to collect.
