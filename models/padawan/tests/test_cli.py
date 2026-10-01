from pathlib import Path

from click.testing import CliRunner
from pytest_mock import MockerFixture

from models.padawan.cli import cli


def _patch_llm(mocker: MockerFixture, response: str) -> None:
    mocker.patch("models.padawan.cli.Settings")
    fake_client = mocker.Mock()
    fake_client.generate.return_value = response
    mocker.patch("models.padawan.cli.AnthropicClient", return_value=fake_client)


def test_generate_writes_output_to_stdout_by_default(tmp_path: Path, mocker: MockerFixture) -> None:
    # Arrange
    _patch_llm(mocker, response="Feature: addition\n")
    source = tmp_path / "add.py"
    source.write_text("def add(a, b):\n    return a + b\n")

    # Act
    result = CliRunner().invoke(cli, ["generate", "--source", str(source)])

    # Assert
    assert result.exit_code == 0
    assert "Feature: addition" in result.output


def test_generate_writes_output_to_the_given_file(tmp_path: Path, mocker: MockerFixture) -> None:
    # Arrange
    _patch_llm(mocker, response="Feature: addition\n")
    source = tmp_path / "add.py"
    source.write_text("def add(a, b):\n    return a + b\n")
    out = tmp_path / "add.feature"

    # Act
    result = CliRunner().invoke(cli, ["generate", "--source", str(source), "--out", str(out)])

    # Assert
    assert result.exit_code == 0
    assert out.read_text() == "Feature: addition\n"
