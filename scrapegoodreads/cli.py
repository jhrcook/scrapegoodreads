"""Scrapegoodreads main entrypoint."""

from typing import Optional

import typer

app = typer.Typer()


@app.command()
def account(id: str) -> None:
    print("getting account info")


@app.command()
def bookshelf(id: str, shelf: Optional[str] = None) -> None:
    print("getting books")


if __name__ == "__main__":
    app()
