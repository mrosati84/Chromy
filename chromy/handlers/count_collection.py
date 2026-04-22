from __future__ import annotations

from chromy.chroma_functions import count_collection
from chromy.command_inputs import CountCollectionInput


def handle_count_collection(command: CountCollectionInput) -> int:
    print(count_collection(command.collection))
    return 0
