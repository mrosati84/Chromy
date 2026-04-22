from __future__ import annotations

from chromy.chroma_functions import create_collection


def handle_create_collection(collection: str) -> int:
    collection_name = create_collection(collection)
    print(f"Created collection '{collection_name}'.")
    return 0
