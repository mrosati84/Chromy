from __future__ import annotations

import io
import unittest
from collections.abc import Callable
from contextlib import redirect_stdout
from pathlib import Path
from typing import TypeVar
from unittest.mock import patch

from chromy.handlers.import_data import handle_import
from chromy.handlers.count_collection import handle_count_collection
from chromy.handlers.create_collection import handle_create_collection
from chromy.handlers.delete_collection import (
    handle_delete_collection,
    handle_delete_records,
)
from chromy.handlers.list_collections import handle_list_collections
from chromy.handlers.query import handle_query

CommandT = TypeVar("CommandT")


class HandlerTests(unittest.TestCase):
    @staticmethod
    def _fixture_path(path: str) -> str:
        return str(Path(path).resolve())

    def test_list_collections_prints_empty_message(self) -> None:
        with patch(
            "chromy.handlers.list_collections.list_collections", return_value=[]
        ):
            exit_code, output = _capture_output(
                handle_list_collections,
            )

        self.assertEqual(exit_code, 0)
        self.assertEqual(output, "No collections found.\n")

    def test_list_collections_prints_collection_names(self) -> None:
        with patch(
            "chromy.handlers.list_collections.list_collections",
            return_value=["notes", "plays"],
        ):
            exit_code, output = _capture_output(
                handle_list_collections,
            )

        self.assertEqual(exit_code, 0)
        self.assertEqual(output, "notes\nplays\n")

    def test_create_collection_uses_typed_input(self) -> None:
        with patch(
            "chromy.handlers.create_collection.create_collection",
            return_value="notes",
        ) as create_collection:
            exit_code, output = _capture_output(
                handle_create_collection,
                "notes",
            )

        create_collection.assert_called_once_with("notes")
        self.assertEqual(exit_code, 0)
        self.assertEqual(output, "Created: collection 'notes'.\n")

    def test_delete_collection_uses_typed_input(self) -> None:
        with patch("chromy.handlers.delete_collection.delete_collection") as delete:
            exit_code, output = _capture_output(
                handle_delete_collection,
                "notes",
            )

        delete.assert_called_once_with("notes")
        self.assertEqual(exit_code, 0)
        self.assertEqual(output, "Deleted collection 'notes'.\n")

    def test_count_collection_uses_typed_input(self) -> None:
        with patch(
            "chromy.handlers.count_collection.count_collection",
            return_value=7,
        ) as count:
            exit_code, output = _capture_output(
                handle_count_collection,
                "notes",
            )

        count.assert_called_once_with("notes")
        self.assertEqual(exit_code, 0)
        self.assertEqual(output, "7\n")

    def test_import_data_uses_typed_input(self) -> None:
        with patch(
            "chromy.handlers.import_data.ingest_file",
            return_value=3,
        ) as ingest_file:
            exit_code, output = _capture_output(
                handle_import,
                "notes",
                "romeo_and_juliet.txt",
            )

        ingest_file.assert_called_once_with(
            "notes",
            self._fixture_path("romeo_and_juliet.txt"),
        )
        self.assertEqual(exit_code, 0)
        self.assertEqual(output, "Added 3 records to collection 'notes'.\n")

    def test_query_uses_typed_input(self) -> None:
        query_result = {"ids": [["1"]], "documents": [["hello"]]}
        with (
            patch("chromy.handlers.query.run_query", return_value=query_result) as run,
            patch(
                "chromy.handlers.query.format_query_result",
                return_value=["Query results:", "1"],
            ) as format_result,
        ):
            exit_code, output = _capture_output(
                handle_query,
                "notes",
                "hello",
            )

        run.assert_called_once_with("notes", "hello")
        format_result.assert_called_once_with(query_result)
        self.assertEqual(exit_code, 0)
        self.assertEqual(output, "Query results:\n1\n")

    def test_delete_records_parses_where_filter(self) -> None:
        with patch(
            "chromy.handlers.delete_collection.delete_data",
            return_value=2,
        ) as delete_data:
            exit_code, output = _capture_output(
                handle_delete_records,
                "notes",
                " file_name = play.txt ",
            )

        delete_data.assert_called_once_with("notes", {"file_name": "play.txt"})
        self.assertEqual(exit_code, 0)
        self.assertEqual(
            output,
            "Deleted 2 record(s) from collection 'notes' where file_name=play.txt.\n",
        )

    def test_delete_records_rejects_invalid_where_filter(self) -> None:
        with self.assertRaisesRegex(
            ValueError,
            "Invalid --where value. Expected <condition>=<value>.",
        ):
            handle_delete_records("notes", "file_name")


def _capture_output(
    handler: Callable[..., int],
    *arguments: CommandT,
) -> tuple[int, str]:
    output = io.StringIO()

    with redirect_stdout(output):
        exit_code = handler(*arguments)

    return exit_code, output.getvalue()


if __name__ == "__main__":
    unittest.main()
