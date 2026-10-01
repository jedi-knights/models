from models.padawan.core.prompts import build_prompt


def test_build_prompt_includes_the_given_source_code() -> None:
    # Arrange
    source = "def add(a: int, b: int) -> int:\n    return a + b\n"

    # Act
    prompt = build_prompt(source)

    # Assert
    assert source in prompt


def test_build_prompt_instructs_pytest_bdd_output() -> None:
    # Arrange
    source = "def noop() -> None: ...\n"

    # Act
    prompt = build_prompt(source)

    # Assert
    assert "pytest-bdd" in prompt.lower()
