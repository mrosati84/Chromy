from __future__ import annotations

from chromy.utilities import format_query_result, print_lines, run_query


def handle_query(collection: str, query_text: str) -> int:
    result = run_query(collection, query_text)
    print_lines(format_query_result(result))
    return 0
