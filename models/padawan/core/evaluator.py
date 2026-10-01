"""Stages generated pytest-bdd output next to its source and runs it."""

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from models.padawan.core.parser import GeneratedTests


@dataclass(frozen=True, slots=True)
class EvalResult:
    """The outcome of running generated tests against real source."""

    passed: bool
    summary: str


class TestRunner(Protocol):
    """Port: anything that can run a staged pytest-bdd suite and report the outcome."""

    def run(self, test_dir: Path) -> EvalResult:
        """Run the suite staged in test_dir and report pass/fail."""
        ...


def stage_eval_fixtures(
    test_dir: Path, module_name: str, source_code: str, generated: GeneratedTests
) -> None:
    """Write the source module, feature file, and step definitions into test_dir.

    Args:
        test_dir: Directory to stage the fixtures in. Must already exist.
        module_name: Name the source module is written under, importable from step defs.
        source_code: The original source under test.
        generated: The parsed feature file and step definitions to pair with it.
    """
    (test_dir / f"{module_name}.py").write_text(source_code)
    (test_dir / "generated.feature").write_text(generated.feature)
    (test_dir / "test_generated.py").write_text(generated.steps)


def evaluate(
    source_code: str,
    module_name: str,
    generated: GeneratedTests,
    runner: TestRunner,
    test_dir: Path,
) -> EvalResult:
    """Stage generated pytest-bdd output against its source and run it.

    Args:
        source_code: The original source under test.
        module_name: Name the source module is staged under.
        generated: The parsed feature file and step definitions to evaluate.
        runner: A TestRunner used to execute the staged suite.
        test_dir: Scratch directory to stage fixtures in. Must already exist.

    Returns:
        Whether the generated suite passed, and a human-readable summary.
    """
    stage_eval_fixtures(test_dir, module_name, source_code, generated)
    return runner.run(test_dir)
