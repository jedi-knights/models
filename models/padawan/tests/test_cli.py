from pathlib import Path

from click.testing import CliRunner
from pytest_mock import MockerFixture

from models.padawan.cli import cli
from models.padawan.core.evaluator import EvalResult


def _patch_llm(mocker: MockerFixture, response: str) -> None:
    mocker.patch("models.padawan.cli.Settings")
    fake_client = mocker.Mock()
    fake_client.generate.return_value = response
    mocker.patch("models.padawan.cli.AnthropicClient", return_value=fake_client)


_STRUCTURED_RESPONSE = (
    "```gherkin\nFeature: addition\n```\n```python\nfrom pytest_bdd import scenarios\n```\n"
)


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


def _patch_eval(mocker: MockerFixture, passed: bool, summary: str) -> None:
    _patch_llm(mocker, response=_STRUCTURED_RESPONSE)
    fake_runner = mocker.Mock()
    fake_runner.run.return_value = EvalResult(passed=passed, summary=summary)
    mocker.patch("models.padawan.cli.SubprocessPytestRunner", return_value=fake_runner)


def test_eval_exits_zero_and_reports_the_summary_when_generated_tests_pass(
    tmp_path: Path, mocker: MockerFixture
) -> None:
    # Arrange
    _patch_eval(mocker, passed=True, summary="1 passed\n")
    source = tmp_path / "calc.py"
    source.write_text("def add(a, b):\n    return a + b\n")

    # Act
    result = CliRunner().invoke(cli, ["eval", "--source", str(source)])

    # Assert
    assert result.exit_code == 0
    assert "1 passed" in result.output


def test_eval_exits_nonzero_when_generated_tests_fail(
    tmp_path: Path, mocker: MockerFixture
) -> None:
    # Arrange
    _patch_eval(mocker, passed=False, summary="1 failed\n")
    source = tmp_path / "calc.py"
    source.write_text("def add(a, b):\n    return a + b\n")

    # Act
    result = CliRunner().invoke(cli, ["eval", "--source", str(source)])

    # Assert
    assert result.exit_code == 1
    assert "1 failed" in result.output
