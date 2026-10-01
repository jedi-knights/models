import subprocess
from pathlib import Path
from types import SimpleNamespace

from pytest_mock import MockerFixture

from models.padawan.adapters.pytest_runner import SubprocessPytestRunner


def test_run_reports_passed_when_pytest_exits_zero(tmp_path: Path, mocker: MockerFixture) -> None:
    # Arrange
    fake_run = mocker.patch("models.padawan.adapters.pytest_runner.subprocess.run")
    fake_run.return_value = SimpleNamespace(returncode=0, stdout="1 passed\n")
    runner = SubprocessPytestRunner()

    # Act
    result = runner.run(tmp_path)

    # Assert
    assert result.passed is True
    assert result.summary == "1 passed\n"
    called_command = fake_run.call_args.args[0]
    assert str(tmp_path) in called_command


def test_run_reports_failed_when_pytest_exits_nonzero(
    tmp_path: Path, mocker: MockerFixture
) -> None:
    # Arrange
    fake_run = mocker.patch("models.padawan.adapters.pytest_runner.subprocess.run")
    fake_run.return_value = SimpleNamespace(returncode=1, stdout="1 failed\n")
    runner = SubprocessPytestRunner()

    # Act
    result = runner.run(tmp_path)

    # Assert
    assert result.passed is False
    assert result.summary == "1 failed\n"


def test_run_reports_failed_on_timeout(tmp_path: Path, mocker: MockerFixture) -> None:
    # Arrange
    fake_run = mocker.patch("models.padawan.adapters.pytest_runner.subprocess.run")
    fake_run.side_effect = subprocess.TimeoutExpired(cmd="pytest", timeout=60)
    runner = SubprocessPytestRunner()

    # Act
    result = runner.run(tmp_path)

    # Assert
    assert result.passed is False
    assert "timed out" in result.summary
