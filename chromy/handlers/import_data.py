from __future__ import annotations

import os
from pathlib import Path

from rich import print

from chromy.errors import UnsupportedTextFileError
from chromy.utilities import ingest_file

from ..utilities import is_probably_text_file


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


def handle_import(collection: str, file: str) -> int:
    absolute_path = _get_absolute_path(file)

    if not is_probably_text_file(absolute_path):
        raise UnsupportedTextFileError()

    records_added = ingest_file(collection, absolute_path)
    print(f"[bold green]Added[/] {records_added} records to collection '{collection}'.")
    return 0
