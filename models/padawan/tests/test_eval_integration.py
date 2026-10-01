"""Integration check: stage real fixtures and run them through a real pytest subprocess.

Every other test mocks either the LLM or the subprocess boundary. This one exercises the
real glue between them — file staging, pytest-bdd's `scenarios()` discovery, and importing
the staged source module — without involving the network.
"""

from pathlib import Path

from models.padawan.adapters.pytest_runner import SubprocessPytestRunner
from models.padawan.core.evaluator import evaluate
from models.padawan.core.parser import GeneratedTests

_SOURCE = "def add(a: int, b: int) -> int:\n    return a + b\n"

_PASSING_STEPS = """\
from pytest_bdd import given, parsers, scenarios, then, when

scenarios("generated.feature")


@given(parsers.parse("two numbers {a:d} and {b:d}"), target_fixture="numbers")
def _given_numbers(a: int, b: int) -> tuple[int, int]:
    return a, b


@when("they are added", target_fixture="result")
def _when_added(numbers: tuple[int, int]) -> int:
    from calc import add

    return add(*numbers)


@then(parsers.parse("the result is {expected:d}"))
def _then_result(result: int, expected: int) -> None:
    assert result == expected
"""

_PASSING_FEATURE = """\
Feature: addition

  Scenario: add two numbers
    Given two numbers 2 and 3
    When they are added
    Then the result is 5
"""

_FAILING_FEATURE = """\
Feature: addition

  Scenario: add two numbers
    Given two numbers 2 and 3
    When they are added
    Then the result is 999
"""


def test_evaluate_passes_for_a_correct_generation(tmp_path: Path) -> None:
    # Arrange
    generated = GeneratedTests(feature=_PASSING_FEATURE, steps=_PASSING_STEPS)

    # Act
    result = evaluate(
        _SOURCE,
        module_name="calc",
        generated=generated,
        runner=SubprocessPytestRunner(),
        test_dir=tmp_path,
    )

    # Assert
    assert result.passed is True, result.summary


def test_evaluate_fails_for_a_generation_with_a_wrong_assertion(tmp_path: Path) -> None:
    # Arrange
    generated = GeneratedTests(feature=_FAILING_FEATURE, steps=_PASSING_STEPS)

    # Act
    result = evaluate(
        _SOURCE,
        module_name="calc",
        generated=generated,
        runner=SubprocessPytestRunner(),
        test_dir=tmp_path,
    )

    # Assert
    assert result.passed is False, result.summary
