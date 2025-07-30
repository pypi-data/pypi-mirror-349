import os
from pathlib import Path
from typing import Annotated

import typer

from confluence_markdown_exporter.confluence import Organization
from confluence_markdown_exporter.confluence import Page
from confluence_markdown_exporter.confluence import Space
from confluence_markdown_exporter.utils.measure_time import measure
from confluence_markdown_exporter.confluence import page_from_url

DEBUG: bool = bool(os.getenv("DEBUG"))

app = typer.Typer()


@app.command()
def page_url(
    page_url: Annotated[str, typer.Argument()],
    output_path: Annotated[Path, typer.Argument()] = Path("."),
) -> None:
    with measure(f"Export page {page_url}"):
        _page = page_from_url(page_url)
        _page.export(output_path)


@app.command()
def page_id(
    page_id: Annotated[int, typer.Argument()],
    output_path: Annotated[Path, typer.Argument()] = Path("."),
) -> None:
    with measure(f"Export page {page_id}"):
        _page = Page.from_id(page_id)
        _page.export(output_path)


@app.command()
def space(
    space_key: Annotated[str, typer.Argument()],
    output_path: Annotated[Path, typer.Argument()] = Path("."),
) -> None:
    with measure(f"Export space {space_key}"):
        space = Space.from_key(space_key)
        space.export(output_path)


@app.command()
def all_spaces(
    output_path: Annotated[Path, typer.Argument()] = Path("."),
) -> None:
    with measure("Export all spaces"):
        org = Organization.from_api()
        org.export(output_path)


if __name__ == "__main__":
    app()
