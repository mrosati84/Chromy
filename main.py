from __future__ import annotations

from chromadb.errors import NotFoundError, InternalError
from chroma_functions import create_collection, delete_collection, list_collections

from cli_parser import build_parser


def main() -> int:
    args = build_parser().parse_args()

    if args.command in {"list-collections", "lc"}:
        collections = list_collections()
        if not collections:
            print("No collections found.")
            return 0

        for name in collections:
            print(name)
        return 0

    if args.command in {"create-collection", "cc"}:
        try:
            create_collection(args.name)
        except InternalError:
            print(f"Collection '{args.name}' already exists.")
            return 1

        print(f"Created collection '{args.name}'.")
        return 0

    if args.command in {"delete-collection", "dc"}:
        try:
            delete_collection(args.name)
        except NotFoundError:
            print(f"Collection '{args.name}' does not exist.")
            return 1

        print(f"Deleted collection '{args.name}'.")
        return 0

    # TODO Implement the count command.

    print("Nothing to do. Use -h to see available commands.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
