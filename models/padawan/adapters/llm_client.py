"""Anthropic-backed implementation of the LLMClient port."""

from anthropic import Anthropic
from anthropic.types import TextBlock

from models.padawan.config import Settings


class AnthropicClient:
    """Generates text via the Anthropic API."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._client = Anthropic(api_key=settings.anthropic_api_key.get_secret_value())

    def generate(self, prompt: str) -> str:
        """Send the prompt to Claude and return its text response.

        Args:
            prompt: The fully-constructed prompt to send.

        Returns:
            The text of the model's response.
        """
        response = self._client.messages.create(
            model=self._settings.model,
            max_tokens=self._settings.max_tokens,
            messages=[{"role": "user", "content": prompt}],
        )
        assert response.content, "Anthropic response had no content blocks"
        block = response.content[0]
        assert isinstance(block, TextBlock), f"expected a text block, got {type(block).__name__}"
        return block.text
