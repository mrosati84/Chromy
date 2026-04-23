from __future__ import annotations
import os
from pathlib import Path

from chromy.utilities import ingest_file


def handle_import(collection: str, file: str) -> int:
    if not os.path.exists(file):
        raise FileNotFoundError()

    # This ensures that the path saved as file_name in the metadatas is the
    # full path rather than a simple file name.
    file_path = Path(file)
    full_file_path = str(file_path.resolve(file_path))

    records_added = ingest_file(collection, full_file_path)
    print(f"Added {records_added} records to collection '{collection}'.")
    return 0
