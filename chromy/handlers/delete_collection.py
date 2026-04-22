from __future__ import annotations

from chromy.chroma_functions import delete_collection, delete_data
from chromy.command_inputs import DeleteCollectionInput, DeleteRecordsInput


def _parse_where_clause(where_clause: str) -> dict[str, str]:
    condition, separator, value = where_clause.partition("=")

    if separator == "":
        raise ValueError("Invalid --where value. Expected <condition>=<value>.")

    condition = condition.strip()
    value = value.strip()

    if not condition or not value:
        raise ValueError("Invalid --where value. Expected <condition>=<value>.")

    return {condition: value}


def handle_delete_collection(command: DeleteCollectionInput) -> int:
    delete_collection(command.collection)
    print(f"Deleted collection '{command.collection}'.")
    return 0


def handle_delete_records(command: DeleteRecordsInput) -> int:
    where = _parse_where_clause(command.where)
    deleted = delete_data(command.collection, where)
    condition, value = next(iter(where.items()))
    print(
        f"Deleted {deleted} record(s) from collection '{command.collection}' "
        f"where {condition}={value}."
    )
    return 0
