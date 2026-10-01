"""Runtime configuration for padawan, loaded from the environment."""

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings for the Anthropic-backed generation client.

    Attributes:
        anthropic_api_key: API key for the Anthropic API.
        model: Claude model identifier to use for generation.
        max_tokens: Maximum tokens to request per generation call.
    """

    model_config = SettingsConfigDict(env_prefix="")

    anthropic_api_key: SecretStr
    model: str = "claude-sonnet-5"
    max_tokens: int = 4096
