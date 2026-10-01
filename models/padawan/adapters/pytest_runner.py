"""Runs a staged pytest-bdd suite as a bounded subprocess."""

import subprocess
import sys
from pathlib import Path

from models.padawan.core.evaluator import EvalResult

# Generated code is untrusted LLM output exercising arbitrary control flow — bound the
# subprocess so a bad generation (e.g. an infinite loop) can't hang the eval run forever.
_TIMEOUT_SECONDS = 60


class SubprocessPytestRunner:
    """Runs pytest against a staged directory in a separate, bounded process."""

    def run(self, test_dir: Path) -> EvalResult:
        """Run pytest against test_dir and report pass/fail.

        Args:
            test_dir: Directory containing the staged source, feature file, and steps.

        Returns:
            Whether the suite passed, and pytest's own summary output.
        """
        try:
            completed = subprocess.run(
                [sys.executable, "-m", "pytest", str(test_dir), "-q"],
                capture_output=True,
                text=True,
                check=False,  # non-zero means test failures, not a crash — branch on returncode
                timeout=_TIMEOUT_SECONDS,
            )
        except subprocess.TimeoutExpired:
            return EvalResult(passed=False, summary=f"timed out after {_TIMEOUT_SECONDS}s")
        return EvalResult(passed=completed.returncode == 0, summary=completed.stdout)
