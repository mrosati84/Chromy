from argparse import Namespace

from chroma_functions import delete_collection, delete_data


def _parse_where_clause(where_clause: str) -> dict[str, str]:
    condition, separator, value = where_clause.partition("=")

    if separator == "":
        raise ValueError("Invalid --where value. Expected <condition>=<value>.")

    condition = condition.strip()
    value = value.strip()

    if not condition or not value:
        raise ValueError("Invalid --where value. Expected <condition>=<value>.")

    return {condition: value}


def handle_delete_collection(args: Namespace) -> int:
    delete_collection(args.collection)
    print(f"Deleted collection '{args.collection}'.")
    return 0


def handle_delete_records(args: Namespace) -> int:
    try:
        where = _parse_where_clause(args.where)
    except ValueError as exc:
        args.error_message = str(exc)
        raise

    deleted = delete_data(args.collection, where)
    condition, value = next(iter(where.items()))
    print(
        f"Deleted {deleted} record(s) from collection '{args.collection}' "
        f"where {condition}={value}."
    )
    return 0
