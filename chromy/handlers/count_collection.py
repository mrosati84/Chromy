from __future__ import annotations

from rich import print
from chromy.chroma_functions import count_collection


def handle_count_collection(collection: str) -> int:
    print(count_collection(collection))
    return 0
