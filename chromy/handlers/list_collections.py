from argparse import Namespace

from chromy.chroma_functions import list_collections
from chromy.utilities import print_lines


def handle_list_collections(_: Namespace) -> int:
    collections = list_collections()
    if not collections:
        print("No collections found.")
        return 0

    print_lines(collections)
    return 0
