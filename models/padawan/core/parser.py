"""Parses generation output into a feature file and step-definition module."""

import re
from dataclasses import dataclass

_GHERKIN_BLOCK = re.compile(r"```gherkin\s*\n(.*?)```", re.DOTALL)
_PYTHON_BLOCK = re.compile(r"```python\s*\n(.*?)```", re.DOTALL)


@dataclass(frozen=True, slots=True)
class GeneratedTests:
    """A parsed feature file paired with its pytest-bdd step definitions."""

    feature: str
    steps: str


def parse_generated_output(text: str) -> GeneratedTests:
    """Extract the feature file and step definitions from generated LLM output.

    Args:
        text: Raw text returned by the LLM, expected to contain one fenced
            ```gherkin block and one fenced ```python block.

    Returns:
        The parsed feature file and step-definition source.

    Raises:
        ValueError: If either fenced block is missing from the text.
    """
    gherkin_match = _GHERKIN_BLOCK.search(text)
    if gherkin_match is None:
        raise ValueError("generated output is missing a ```gherkin block")

    python_match = _PYTHON_BLOCK.search(text)
    if python_match is None:
        raise ValueError("generated output is missing a ```python block")

    return GeneratedTests(
        feature=gherkin_match.group(1).strip() + "\n",
        steps=python_match.group(1).strip() + "\n",
    )
