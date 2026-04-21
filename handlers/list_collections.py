from argparse import Namespace

from chroma_functions import list_collections
from utilities import print_lines


def handle_list_collections(_: Namespace) -> int:
    collections = list_collections()
    if not collections:
        print("No collections found.")
        return 0

    print_lines(collections)
    return 0
