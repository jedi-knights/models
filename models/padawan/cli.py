"""Command-line entrypoint for padawan."""

from pathlib import Path

import click

from models.padawan.adapters.llm_client import AnthropicClient
from models.padawan.config import Settings
from models.padawan.core.generator import generate_bdd_tests


@click.group()
def cli() -> None:
    """Padawan: generate pytest-bdd tests from Python source."""


@cli.command()
@click.option(
    "--source",
    "source_path",
    required=True,
    type=click.Path(exists=True, dir_okay=False),
    help="Path to the Python source module to generate tests for.",
)
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
    # anthropic_api_key is loaded from env by pydantic-settings, not passed as a constructor arg
    settings = Settings()  # type: ignore[call-arg]
    client = AnthropicClient(settings)
    result = generate_bdd_tests(source_code, client=client)

    if out_path:
        Path(out_path).write_text(result)
    else:
        click.echo(result)


if __name__ == "__main__":
    cli()
