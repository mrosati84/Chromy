from __future__ import annotations

from chromy.command_inputs import QueryInput
from chromy.utilities import format_query_result, print_lines, run_query


def handle_query(command: QueryInput) -> int:
    result = run_query(command.collection, command.query_text)
    print_lines(format_query_result(result))
    return 0
