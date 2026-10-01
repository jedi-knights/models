from models.padawan.core.generator import generate_bdd_tests


class FakeLLMClient:
    """In-memory LLMClient stand-in — records the prompt it was asked to generate from."""

    def __init__(self, response: str) -> None:
        self.response = response
        self.last_prompt: str | None = None

    def generate(self, prompt: str) -> str:
        self.last_prompt = prompt
        return self.response


def test_generate_bdd_tests_returns_the_clients_response() -> None:
    # Arrange
    client = FakeLLMClient(response="Feature: addition\n")
    source = "def add(a: int, b: int) -> int:\n    return a + b\n"

    # Act
    result = generate_bdd_tests(source, client=client)

    # Assert
    assert result == "Feature: addition\n"


def test_generate_bdd_tests_sends_the_source_code_to_the_client() -> None:
    # Arrange
    client = FakeLLMClient(response="")
    source = "def add(a: int, b: int) -> int:\n    return a + b\n"

    # Act
    generate_bdd_tests(source, client=client)

    # Assert
    assert client.last_prompt is not None
    assert source in client.last_prompt
