import json
import sys
from pathlib import Path
from typing import Annotated

import typer
import yaml

from app.analyzer import analyze_instructions
from app.parser import parse_dockerfile

app = typer.Typer()


@app.command()
def executor(
    dockerfile: Annotated[Path, typer.Argument(help="Path to Dockerfile")],
    analyze: Annotated[bool, typer.Option("-a", "--analyze", help="Run detailed instruction-level analysis")] = False,
    parse: Annotated[bool, typer.Option("-p", "--parse", help="Parse and output the Dockerfile")] = False,
    parse_output: Annotated[
        str,
        typer.Option(
            "--output",
            "-o",
            help="Output format for parse command (json or yaml)",
            show_default=True,
            case_sensitive=False,
        ),
    ] = "json",
):
    if analyze:
        typer.echo(f"Running analysis on: {dockerfile}")
        parse_data = parse_dockerfile(dockerfile)
        issues = analyze_instructions(parse_data)
        if not issues:
            typer.echo("✅ No issues found.")
        else:
            typer.echo(json.dumps(issues, indent=2))
    if parse:
        output_format = parse_output.lower()
        if output_format not in ("json", "yaml"):
            typer.echo(f"Error: Unsupported output format '{parse_output}'. Use 'json' or 'yaml'.", err=True)
            raise typer.Exit(code=1)
        typer.echo(f"Parsing {dockerfile} and outputting as {output_format}")
        parse_data = parse_dockerfile(dockerfile)
        if output_format == "json":
            typer.echo(json.dumps(parse_data, indent=2))
        else:
            typer.echo(yaml.dump(parse_data))
    if not (analyze or parse):
        typer.echo("Please specify --analyze or --parse")


if __name__ == "__main__":
    # If no command is provided, insert the default command 'parser' automatically
    if len(sys.argv) == 1 or (len(sys.argv) == 2 and not sys.argv[1].startswith("-")):
        sys.argv.insert(1, "parser")
    app()
