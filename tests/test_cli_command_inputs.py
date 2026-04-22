from __future__ import annotations

import io
import unittest
from argparse import Namespace
from contextlib import redirect_stdout

from chromy.cli_app import build_command_input, execute_command
from chromy.cli_parser import build_parser
from chromy.command_inputs import (
    AddDataInput,
    CountCollectionInput,
    CreateCollectionInput,
    DeleteCollectionInput,
    DeleteRecordsInput,
    ListCollectionsInput,
    QueryInput,
)


class BuildCommandInputTests(unittest.TestCase):
    def test_parser_converts_list_collections_and_alias(self) -> None:
        self.assertEqual(_parse_input(["list-collections"]), ListCollectionsInput())
        self.assertEqual(_parse_input(["lc"]), ListCollectionsInput())

    def test_parser_converts_create_collection_and_alias(self) -> None:
        expected = CreateCollectionInput(collection="notes")

        self.assertEqual(_parse_input(["create-collection", "notes"]), expected)
        self.assertEqual(_parse_input(["cc", "notes"]), expected)

    def test_parser_converts_delete_collection_and_alias(self) -> None:
        expected = DeleteCollectionInput(collection="notes")

        self.assertEqual(_parse_input(["delete-collection", "notes"]), expected)
        self.assertEqual(_parse_input(["dc", "notes"]), expected)

    def test_parser_converts_count_and_alias(self) -> None:
        expected = CountCollectionInput(collection="notes")

        self.assertEqual(_parse_input(["count", "notes"]), expected)
        self.assertEqual(_parse_input(["co", "notes"]), expected)

    def test_parser_converts_add_data_and_alias(self) -> None:
        expected = AddDataInput(collection="notes", file="romeo_and_juliet.txt")

        self.assertEqual(
            _parse_input(["add-data", "notes", "romeo_and_juliet.txt"]),
            expected,
        )
        self.assertEqual(
            _parse_input(["ad", "notes", "romeo_and_juliet.txt"]),
            expected,
        )

    def test_parser_converts_query_and_alias(self) -> None:
        expected = QueryInput(collection="notes", query_text="Where is Romeo?")

        self.assertEqual(
            _parse_input(["query", "notes", "Where is Romeo?"]),
            expected,
        )
        self.assertEqual(_parse_input(["q", "notes", "Where is Romeo?"]), expected)

    def test_parser_converts_delete_records_and_alias(self) -> None:
        expected = DeleteRecordsInput(collection="notes", where="file_name=play.txt")

        self.assertEqual(
            _parse_input(["delete", "notes", "--where", "file_name=play.txt"]),
            expected,
        )
        self.assertEqual(
            _parse_input(["del", "notes", "--where", "file_name=play.txt"]),
            expected,
        )

    def test_invalid_delete_filter_keeps_user_facing_error(self) -> None:
        args = Namespace(command="delete", collection="notes", where="file_name")
        output = io.StringIO()

        with redirect_stdout(output):
            exit_code = execute_command(args)

        self.assertEqual(exit_code, 1)
        self.assertEqual(
            output.getvalue().strip(),
            "Invalid --where value. Expected <condition>=<value>.",
        )
        self.assertFalse(hasattr(args, "error_message"))


def _parse_input(argv: list[str]) -> object:
    return build_command_input(build_parser().parse_args(argv))


if __name__ == "__main__":
    unittest.main()
