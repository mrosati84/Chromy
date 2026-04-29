from __future__ import annotations

from rich import print

from chromy.chroma_functions import count_collection
from chromy.output import format_count_message


def handle_count_collection(collection: str) -> int:
    print(format_count_message(collection, count_collection(collection)))
    return 0
