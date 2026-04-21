from argparse import Namespace

from utilities import format_query_result, print_lines, run_query


def handle_query(args: Namespace) -> int:
    result = run_query(args.collection, args.query_text)
    print_lines(format_query_result(result))
    return 0
