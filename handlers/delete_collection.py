from argparse import Namespace

from chroma_functions import delete_collection


def handle_delete_collection(args: Namespace) -> int:
    delete_collection(args.collection)
    print(f"Deleted collection '{args.collection}'.")
    return 0
