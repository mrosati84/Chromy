from __future__ import annotations

from chromy.utilities import ingest_file


def handle_add_data(collection: str, file: str) -> int:
    records_added = ingest_file(collection, file)
    print(f"Added {records_added} records to collection '{collection}'.")
    return 0
