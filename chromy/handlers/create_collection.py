from __future__ import annotations

from rich import print
from chromy.chroma_functions import create_collection


def handle_create_collection(collection: str) -> int:
    collection_name = create_collection(collection)
    print(f"[bold green]Created[/]: collection '{collection_name}'.")
    return 0
