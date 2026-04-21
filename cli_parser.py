import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Inspect local Chroma collections.")
    subparsers = parser.add_subparsers(dest="command")

    # List existing collections
    subparsers.add_parser(
        "list-collections",
        aliases=["lc"],
        help="List all collections stored in the local Chroma database.",
    )

    # Create a new collection
    create_parser = subparsers.add_parser(
        "create-collection",
        aliases=["cc"],
        help="Create a collection in the local Chroma database.",
    )
    create_parser.add_argument("name", help="Name of the collection to create.")

    # Delete a collection
    delete_parser = subparsers.add_parser(
        "delete-collection",
        aliases=["dc"],
        help="Delete a collection from the local Chroma database.",
    )
    delete_parser.add_argument("name", help="Name of the collection to delete.")

    # Count documents in a collection
    count_parser = subparsers.add_parser(
        "count",
        aliases=["co"],
        help="Count records in a collection from the local Chroma database.",
    )
    count_parser.add_argument("name", help="Name of the collection to count.")

    # Add documents to a collection
    add_parser = subparsers.add_parser(
        "add-data",
        aliases=["ad"],
        help="Chunk, embed, and add a file to a collection in the local Chroma database.",
    )
    add_parser.add_argument("collection", help="Name of the target collection.")
    add_parser.add_argument(
        "file", help="Path to the file to chunk and add to the collection."
    )

    # Query doc
    query_parser = subparsers.add_parser(
        "query",
        aliases=["q"],
        help="Query a collection with given text/s.",
    )
    query_parser.add_argument("collection", help="Name of the target collection.")
    query_parser.add_argument("texts", help="The text/s to query.")

    return parser
