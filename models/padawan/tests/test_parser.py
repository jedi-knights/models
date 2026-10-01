import pytest

from models.padawan.core.parser import parse_generated_output


def test_parse_generated_output_extracts_the_feature_block() -> None:
    # Arrange
    text = (
        "Here you go:\n\n"
        "```gherkin\nFeature: addition\n```\n\n"
        "```python\nfrom pytest_bdd import scenarios\n```\n"
    )

    # Act
    result = parse_generated_output(text)

    # Assert
    assert result.feature == "Feature: addition\n"


def test_parse_generated_output_extracts_the_steps_block() -> None:
    # Arrange
    text = "```gherkin\nFeature: addition\n```\n```python\nfrom pytest_bdd import scenarios\n```\n"

    # Act
    result = parse_generated_output(text)

    # Assert
    assert result.steps == "from pytest_bdd import scenarios\n"


def test_parse_generated_output_raises_when_gherkin_block_missing() -> None:
    # Arrange
    text = "```python\nfrom pytest_bdd import scenarios\n```\n"

    # Act / Assert
    with pytest.raises(ValueError, match="gherkin"):
        parse_generated_output(text)


def test_parse_generated_output_raises_when_python_block_missing() -> None:
    # Arrange
    text = "```gherkin\nFeature: addition\n```\n"

    # Act / Assert
    with pytest.raises(ValueError, match="python"):
        parse_generated_output(text)
