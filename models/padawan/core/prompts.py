"""Prompt construction for pytest-bdd generation requests."""

_SYSTEM_PREAMBLE = (
    "You are an expert Python test engineer. Given a Python source module, "
    "generate a pytest-bdd feature file and matching step definitions that "
    "exercise its public behavior. Follow pytest-bdd conventions: Given/When/Then "
    "steps registered via @given/@when/@then, fixtures for shared state, and a "
    ".feature file using Gherkin syntax."
)


def build_prompt(source_code: str) -> str:
    """Build the LLM prompt requesting pytest-bdd tests for the given source.

    Args:
        source_code: The Python source module to generate tests for.

    Returns:
        A complete prompt string ready to send to an LLM client.
    """
    return f"{_SYSTEM_PREAMBLE}\n\nSource code:\n```python\n{source_code}\n```\n"
