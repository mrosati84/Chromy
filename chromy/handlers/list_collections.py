from __future__ import annotations

from chromy.chroma_functions import list_collections
from chromy.command_inputs import ListCollectionsInput
from chromy.utilities import print_lines


def handle_list_collections(_: ListCollectionsInput) -> int:
    collections = list_collections()
    if not collections:
        print("No collections found.")
        return 0

    print_lines(collections)
    return 0
