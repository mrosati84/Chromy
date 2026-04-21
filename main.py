from __future__ import annotations

from chromadb.errors import InternalError, NotFoundError
from dotenv import load_dotenv

from chroma_functions import (
    add_data,
    count_collection,
    create_collection,
    delete_collection,
    list_collections,
)
from chunk_functions import chunk_file
from cli_parser import build_parser
from embed import embed

load_dotenv()


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
            collection = create_collection(args.name)
        except InternalError:
            print(f"Collection '{args.name}' already exists.")
            return 1

        print(f"Created collection '{collection}'.")

        return 0

    if args.command in {"delete-collection", "dc"}:
        try:
            delete_collection(args.name)
        except NotFoundError:
            print(f"Collection '{args.name}' does not exist.")
            return 1

        print(f"Deleted collection '{args.name}'.")

        return 0

    if args.command in {"count", "co"}:
        try:
            count = count_collection(args.name)
        except NotFoundError:
            print(f"Collection '{args.name}' does not exist.")
            return 1

        print(count)

        return 0

    if args.command in {"add-data", "ad"}:
        try:
            chunks = chunk_file(args.file)
            embeddings = embed(chunks)
            add_data(args.collection, embeddings)
        except NotFoundError:
            print(f"Collection '{args.collection}' does not exist.")
            return 1
        except FileNotFoundError:
            print(f"The file {args.file} was not found.")
            return 1

        print(f"Added {len(embeddings)} records to collection '{args.collection}'.")

        return 0

    print("Nothing to do. Use -h to see available commands.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
