import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Inspect local Chroma collections.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser(
        "list-collections",
        aliases=["lc"],
        help="List all collections stored in the local Chroma database.",
    )

    create_parser = subparsers.add_parser(
        "create-collection",
        aliases=["cc"],
        help="Create a collection in the local Chroma database.",
    )
    create_parser.add_argument("name", help="Name of the collection to create.")

    delete_parser = subparsers.add_parser(
        "delete-collection",
        aliases=["dc"],
        help="Delete a collection from the local Chroma database.",
    )
    delete_parser.add_argument("name", help="Name of the collection to delete.")

    count_parser = subparsers.add_parser(
        "count",
        aliases=["co"],
        help="Count records in a collection from the local Chroma database.",
    )
    count_parser.add_argument("name", help="Name of the collection to count.")

    add_parser = subparsers.add_parser(
        "add-data",
        aliases=["ad"],
        help="Chunk, embed, and add a file to a collection in the local Chroma database.",
    )
    add_parser.add_argument("collection", help="Name of the target collection.")
    add_parser.add_argument("file", help="Path to the file to chunk and add to the collection.")

    return parser
