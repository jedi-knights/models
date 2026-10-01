from models.padawan.core.prompts import build_prompt


def test_build_prompt_includes_the_given_source_code() -> None:
    # Arrange
    source = "def add(a: int, b: int) -> int:\n    return a + b\n"

    # Act
    prompt = build_prompt(source, module_name="calc")

    # Assert
    assert source in prompt


def test_build_prompt_instructs_pytest_bdd_output() -> None:
    # Arrange
    source = "def noop() -> None: ...\n"

    # Act
    prompt = build_prompt(source, module_name="calc")

    # Assert
    assert "pytest-bdd" in prompt.lower()


def test_build_prompt_names_the_module_steps_should_import_from() -> None:
    # Arrange
    source = "def noop() -> None: ...\n"

    # Act
    prompt = build_prompt(source, module_name="calc")

    # Assert
    assert "calc" in prompt


def test_build_prompt_requests_the_structured_block_format() -> None:
    # Arrange
    source = "def noop() -> None: ...\n"

    # Act
    prompt = build_prompt(source, module_name="calc")

    # Assert
    assert "```gherkin" in prompt
    assert "```python" in prompt
