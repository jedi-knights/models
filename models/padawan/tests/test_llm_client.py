from types import SimpleNamespace

from anthropic.types import TextBlock
from pydantic import SecretStr
from pytest_mock import MockerFixture

from models.padawan.adapters.llm_client import AnthropicClient
from models.padawan.config import Settings


def test_anthropic_client_sends_the_prompt_as_a_user_message(mocker: MockerFixture) -> None:
    # Arrange
    fake_response = SimpleNamespace(content=[TextBlock(type="text", text="Feature: addition\n")])
    fake_anthropic = mocker.patch("models.padawan.adapters.llm_client.Anthropic")
    fake_anthropic.return_value.messages.create.return_value = fake_response
    settings = Settings(
        anthropic_api_key=SecretStr("test-key"), model="claude-test", max_tokens=123
    )
    client = AnthropicClient(settings)

    # Act
    result = client.generate("generate tests for this")

    # Assert
    fake_anthropic.return_value.messages.create.assert_called_once_with(
        model="claude-test",
        max_tokens=123,
        messages=[{"role": "user", "content": "generate tests for this"}],
    )
    assert result == "Feature: addition\n"
