"""Orchestrates pytest-bdd generation: builds a prompt and delegates to an LLM client."""

from typing import Protocol

from models.padawan.core.prompts import build_prompt


class LLMClient(Protocol):
    """Port: anything that can turn a prompt into generated text."""

    def generate(self, prompt: str) -> str:
        """Generate text for the given prompt."""
        ...


def generate_bdd_tests(source_code: str, client: LLMClient) -> str:
    """Generate a pytest-bdd feature file and step definitions for the given source.

    Args:
        source_code: The Python source module to generate tests for.
        client: An LLMClient used to perform the actual generation.

    Returns:
        The LLM's generated pytest-bdd output.
    """
    prompt = build_prompt(source_code)
    return client.generate(prompt)
