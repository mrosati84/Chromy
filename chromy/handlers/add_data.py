from __future__ import annotations

from chromy.command_inputs import AddDataInput
from chromy.utilities import ingest_file


def handle_add_data(command: AddDataInput) -> int:
    records_added = ingest_file(command.collection, command.file)
    print(f"Added {records_added} records to collection '{command.collection}'.")
    return 0
