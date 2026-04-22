from argparse import Namespace

from chromy.utilities import ingest_file


def handle_add_data(args: Namespace) -> int:
    records_added = ingest_file(args.collection, args.file)
    print(f"Added {records_added} records to collection '{args.collection}'.")
    return 0
