from argparse import Namespace

from chromy.chroma_functions import create_collection


def handle_create_collection(args: Namespace) -> int:
    collection_name = create_collection(args.collection)
    print(f"Created collection '{collection_name}'.")
    return 0
