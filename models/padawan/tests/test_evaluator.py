from pathlib import Path

from models.padawan.core.evaluator import EvalResult, evaluate
from models.padawan.core.parser import GeneratedTests


class FakeTestRunner:
    """In-memory TestRunner stand-in — records the directory it was asked to run."""

    def __init__(self, result: EvalResult) -> None:
        self.result = result
        self.last_test_dir: Path | None = None

    def run(self, test_dir: Path) -> EvalResult:
        self.last_test_dir = test_dir
        return self.result


def test_evaluate_stages_the_source_feature_and_steps(tmp_path: Path) -> None:
    # Arrange
    generated = GeneratedTests(
        feature="Feature: addition\n", steps="from pytest_bdd import scenarios\n"
    )
    runner = FakeTestRunner(EvalResult(passed=True, summary="1 passed"))

    # Act
    evaluate(
        "def add(a, b):\n    return a + b\n",
        module_name="calc",
        generated=generated,
        runner=runner,
        test_dir=tmp_path,
    )

    # Assert
    assert (tmp_path / "calc.py").read_text() == "def add(a, b):\n    return a + b\n"
    assert (tmp_path / "generated.feature").read_text() == "Feature: addition\n"
    assert (tmp_path / "test_generated.py").read_text() == "from pytest_bdd import scenarios\n"


def test_evaluate_returns_the_runners_result(tmp_path: Path) -> None:
    # Arrange
    generated = GeneratedTests(
        feature="Feature: addition\n", steps="from pytest_bdd import scenarios\n"
    )
    runner = FakeTestRunner(EvalResult(passed=True, summary="1 passed"))

    # Act
    result = evaluate("", module_name="calc", generated=generated, runner=runner, test_dir=tmp_path)

    # Assert
    assert result == EvalResult(passed=True, summary="1 passed")
    assert runner.last_test_dir == tmp_path
