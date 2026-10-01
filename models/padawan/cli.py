"""Command-line entrypoint for padawan."""

import sys
import tempfile
from pathlib import Path

import click

from models.padawan.adapters.llm_client import AnthropicClient
from models.padawan.adapters.pytest_runner import SubprocessPytestRunner
from models.padawan.config import Settings
from models.padawan.core.evaluator import evaluate
from models.padawan.core.generator import generate_bdd_tests
from models.padawan.core.parser import parse_generated_output

_SOURCE_OPTION = click.option(
    "--source",
    "source_path",
    required=True,
    type=click.Path(exists=True, dir_okay=False),
    help="Path to the Python source module to generate tests for.",
)


@click.group()
def cli() -> None:
    """Padawan: generate pytest-bdd tests from Python source."""


@cli.command()
@_SOURCE_OPTION
@click.option(
    "--out",
    "out_path",
    type=click.Path(dir_okay=False),
    default=None,
    help="Path to write the generated output. Defaults to stdout.",
)
def generate(source_path: str, out_path: str | None) -> None:
    """Generate a pytest-bdd feature file and steps for SOURCE."""
    source_code = Path(source_path).read_text()
    module_name = Path(source_path).stem
    # anthropic_api_key is loaded from env by pydantic-settings, not passed as a constructor arg
    settings = Settings()  # type: ignore[call-arg]
    client = AnthropicClient(settings)
    result = generate_bdd_tests(source_code, module_name, client=client)

    if out_path:
        Path(out_path).write_text(result)
    else:
        click.echo(result)


@cli.command("eval")
@_SOURCE_OPTION
def eval_command(source_path: str) -> None:
    """Generate pytest-bdd tests for SOURCE and run them against it."""
    source_code = Path(source_path).read_text()
    module_name = Path(source_path).stem
    # anthropic_api_key is loaded from env by pydantic-settings, not passed as a constructor arg
    settings = Settings()  # type: ignore[call-arg]
    client = AnthropicClient(settings)
    raw_output = generate_bdd_tests(source_code, module_name, client=client)
    generated = parse_generated_output(raw_output)

    with tempfile.TemporaryDirectory() as workdir:
        result = evaluate(
            source_code,
            module_name,
            generated,
            runner=SubprocessPytestRunner(),
            test_dir=Path(workdir),
        )

    click.echo(result.summary)
    if not result.passed:
        sys.exit(1)


if __name__ == "__main__":
    cli()
