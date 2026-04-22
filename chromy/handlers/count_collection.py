from argparse import Namespace

from chromy.chroma_functions import count_collection


def handle_count_collection(args: Namespace) -> int:
    print(count_collection(args.collection))
    return 0
