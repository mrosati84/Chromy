from __future__ import annotations

from typing import Annotated, Callable

import typer
from chromadb.errors import InternalError, NotFoundError
from rich import print

from chromy.errors import ChromaPathError
from chromy.handlers.count_collection import handle_count_collection
from chromy.handlers.create_collection import handle_create_collection
from chromy.handlers.delete_collection import (
    handle_delete_collection,
    handle_delete_records,
)
from chromy.handlers.import_data import handle_import
from chromy.handlers.list_collections import handle_list_collections
from chromy.handlers.query import handle_query

app = typer.Typer(help="Chromy, local RAG CLI based on Chromadb.")

ExitCodeHandler = Callable[[], int]


def _run(handler: ExitCodeHandler) -> None:
    try:
        exit_code = handler()
    except ChromaPathError as exc:
        _fail(str(exc))

    if exit_code != 0:
        raise typer.Exit(exit_code)


def _fail(message: str) -> None:
    print("[bold red]Error[/]:", message)
    raise typer.Exit(1)


# ------------------------------------------------------------------------------
# LIST COLLECTIONS
# ------------------------------------------------------------------------------
@app.command(
    "list-collections",
    help="List all collections stored in the local Chroma database.",
)
def list_collections() -> None:
    _run(handle_list_collections)


# ------------------------------------------------------------------------------
# CREATE A COLLECTION
# ------------------------------------------------------------------------------
@app.command(
    "create-collection",
    help="Create a collection in the local Chroma database.",
)
def create_collection(
    collection: Annotated[
        str,
        typer.Argument(help="Name of the collection to create."),
    ],
) -> None:
    try:
        _run(lambda: handle_create_collection(collection))
    except InternalError:
        _fail(f"Collection '{collection}' already exists.")


# ------------------------------------------------------------------------------
# DELETE A COLLECTION
# ------------------------------------------------------------------------------
@app.command(
    "delete-collection",
    help="Delete a collection from the local Chroma database.",
)
def delete_collection(
    collection: Annotated[
        str,
        typer.Argument(help="Name of the collection to delete."),
    ],
) -> None:
    try:
        _run(lambda: handle_delete_collection(collection))
    except NotFoundError:
        _fail(f"Collection '{collection}' does not exist.")


# ------------------------------------------------------------------------------
# COUNT RECORDS
# ------------------------------------------------------------------------------
@app.command(
    "count",
    help="Count records in a collection from the local Chroma database.",
)
def count(
    collection: Annotated[
        str,
        typer.Argument(help="Name of the collection to count."),
    ],
) -> None:
    try:
        _run(lambda: handle_count_collection(collection))
    except NotFoundError:
        _fail(f"Collection '{collection}' does not exist.")


# ------------------------------------------------------------------------------
# IMPORT DATA
# ------------------------------------------------------------------------------
@app.command(
    "import",
    help=(
        "Chunk, embed, and add one or more files to a collection in the "
        "local Chroma database."
    ),
)
def import_data(
    collection: Annotated[
        str,
        typer.Argument(help="Name of the target collection."),
    ],
    files: Annotated[
        list[str],
        typer.Argument(
            help="Path(s) to the file(s) to chunk and add to the collection."
        ),
    ],
) -> None:
    try:
        _run(lambda: handle_import(collection, files))
    except NotFoundError:
        _fail(f"Collection '{collection}' does not exist.")


# ------------------------------------------------------------------------------
# QUERY
# ------------------------------------------------------------------------------
@app.command("query", help="Query a collection with the provided text.")
def query(
    collection: Annotated[
        str,
        typer.Argument(help="Name of the target collection."),
    ],
    query_text: Annotated[
        str,
        typer.Argument(help="The text to query."),
    ],
) -> None:
    try:
        _run(lambda: handle_query(collection, query_text))
    except NotFoundError:
        _fail(f"Collection '{collection}' does not exist.")


# ------------------------------------------------------------------------------
# DELETE DATA
# ------------------------------------------------------------------------------
@app.command("delete", help="Delete records from a collection using a metadata filter.")
def delete_records(
    collection: Annotated[
        str,
        typer.Argument(help="Name of the target collection."),
    ],
    where: Annotated[
        str,
        typer.Option(
            "--where",
            help="Metadata filter in the format <condition>=<value>.",
            metavar="CONDITION=VALUE",
        ),
    ],
) -> None:
    try:
        _run(lambda: handle_delete_records(collection, where))
    except NotFoundError:
        _fail(f"Collection '{collection}' does not exist.")
    except ValueError as exc:
        _fail(str(exc))
