from __future__ import annotations

import os
from pathlib import Path
from typing import Final

from rich import print

from chromy.errors import UnsupportedTextFileError
from chromy.utilities import ingest_file

from ..utilities import is_probably_text_file

SUCCESS_EXIT_CODE: Final = 0
FAILURE_EXIT_CODE: Final = 1


def _get_absolute_path(file: str) -> str:
    """
    A helper method that, given a valid relative path to a file, returns its
    absolute path.

    Args:
        file (str): The relative path to the file.

    Raises:
        FileNotFoundError(): If the file does not exist.
    """
    if not os.path.exists(file):
        raise FileNotFoundError()

    file_path = Path(file)
    return str(file_path.resolve())


def _import_one(collection: str, file: str) -> int:
    absolute_path = _get_absolute_path(file)

    if not Path(absolute_path).is_file():
        raise FileNotFoundError()

    if not is_probably_text_file(absolute_path):
        raise UnsupportedTextFileError()

    records_added = ingest_file(collection, absolute_path)
    print(
        "[bold green]Added[/] "
        f"{records_added} records from '{file}' to collection '{collection}'."
    )
    return SUCCESS_EXIT_CODE


def handle_import(collection: str, files: list[str]) -> int:
    successful_imports = 0
    failed_imports = 0
    seen_paths: set[str] = set()

    for file in files:
        try:
            absolute_path = _get_absolute_path(file)
            if absolute_path in seen_paths:
                continue

            seen_paths.add(absolute_path)
            _import_one(collection, file)
            successful_imports += 1
        except FileNotFoundError:
            failed_imports += 1
            print(f"[bold red]Error[/]: The file '{file}' was not found.")
        except UnsupportedTextFileError:
            failed_imports += 1
            print(f"[bold red]Error[/]: The file '{file}' is not a text file.")

    print(
        f"Imported {successful_imports} file(s) successfully; {failed_imports} failed."
    )

    if failed_imports:
        return FAILURE_EXIT_CODE

    return SUCCESS_EXIT_CODE
