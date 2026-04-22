from __future__ import annotations

from chromy.chroma_functions import create_collection
from chromy.command_inputs import CreateCollectionInput


def handle_create_collection(command: CreateCollectionInput) -> int:
    collection_name = create_collection(command.collection)
    print(f"Created collection '{collection_name}'.")
    return 0
