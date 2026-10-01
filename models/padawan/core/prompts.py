"""Prompt construction for pytest-bdd generation requests."""

_SYSTEM_PREAMBLE = (
    "You are an expert Python test engineer. Given a Python source module, "
    "generate a pytest-bdd feature file and matching step definitions that "
    "exercise its public behavior. Respond with exactly two fenced code blocks "
    "and nothing else: a ```gherkin block containing the complete .feature file, "
    "and a ```python block containing the step definitions. The python block must "
    "begin with `from pytest_bdd import scenarios, given, when, then`, call "
    '`scenarios("generated.feature")`, and import anything it needs to exercise '
    "from a module named {module_name}."
)


def build_prompt(source_code: str, module_name: str) -> str:
    """Build the LLM prompt requesting pytest-bdd tests for the given source.

    Args:
        source_code: The Python source module to generate tests for.
        module_name: The module name step definitions should import the source from.

    Returns:
        A complete prompt string ready to send to an LLM client.
    """
    preamble = _SYSTEM_PREAMBLE.format(module_name=module_name)
    return f"{preamble}\n\nSource code:\n```python\n{source_code}\n```\n"
