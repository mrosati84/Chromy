from __future__ import annotations

import unittest
from collections.abc import Sequence
from unittest.mock import patch

from click.testing import Result
from typer.testing import CliRunner

from chromy.cli import app


class CliTests(unittest.TestCase):
    def test_list_collections_and_alias(self) -> None:
        for command in ("list-collections", "lc"):
            with patch(
                "chromy.handlers.list_collections.list_collections",
                return_value=[],
            ):
                result = _invoke([command])

            self.assertEqual(result.exit_code, 0)
            self.assertEqual(result.stdout, "No collections found.\n")

    def test_create_collection_and_alias(self) -> None:
        for command in ("create-collection", "cc"):
            with patch(
                "chromy.handlers.create_collection.create_collection",
                return_value="notes",
            ) as create_collection:
                result = _invoke([command, "notes"])

            create_collection.assert_called_once_with("notes")
            self.assertEqual(result.exit_code, 0)
            self.assertEqual(result.stdout, "Created collection 'notes'.\n")

    def test_delete_collection_and_alias(self) -> None:
        for command in ("delete-collection", "dc"):
            with patch(
                "chromy.handlers.delete_collection.delete_collection",
            ) as delete_collection:
                result = _invoke([command, "notes"])

            delete_collection.assert_called_once_with("notes")
            self.assertEqual(result.exit_code, 0)
            self.assertEqual(result.stdout, "Deleted collection 'notes'.\n")

    def test_count_and_alias(self) -> None:
        for command in ("count", "co"):
            with patch(
                "chromy.handlers.count_collection.count_collection",
                return_value=7,
            ) as count_collection:
                result = _invoke([command, "notes"])

            count_collection.assert_called_once_with("notes")
            self.assertEqual(result.exit_code, 0)
            self.assertEqual(result.stdout, "7\n")

    def test_add_data_and_alias(self) -> None:
        for command in ("add-data", "ad"):
            with patch(
                "chromy.handlers.add_data.ingest_file",
                return_value=3,
            ) as ingest_file:
                result = _invoke([command, "notes", "romeo_and_juliet.txt"])

            ingest_file.assert_called_once_with("notes", "romeo_and_juliet.txt")
            self.assertEqual(result.exit_code, 0)
            self.assertEqual(result.stdout, "Added 3 records to collection 'notes'.\n")

    def test_query_and_alias(self) -> None:
        query_result = {"ids": [["1"]], "documents": [["hello"]]}

        for command in ("query", "q"):
            with (
                patch(
                    "chromy.handlers.query.run_query", return_value=query_result
                ) as run,
                patch(
                    "chromy.handlers.query.format_query_result",
                    return_value=["Query results:", "1"],
                ) as format_result,
            ):
                result = _invoke([command, "notes", "Where is Romeo?"])

            run.assert_called_once_with("notes", "Where is Romeo?")
            format_result.assert_called_once_with(query_result)
            self.assertEqual(result.exit_code, 0)
            self.assertEqual(result.stdout, "Query results:\n1\n")

    def test_delete_records_and_alias(self) -> None:
        for command in ("delete", "del"):
            with patch(
                "chromy.handlers.delete_collection.delete_data",
                return_value=2,
            ) as delete_data:
                result = _invoke(
                    [command, "notes", "--where", " file_name = play.txt "],
                )

            delete_data.assert_called_once_with("notes", {"file_name": "play.txt"})
            self.assertEqual(result.exit_code, 0)
            self.assertEqual(
                result.stdout,
                "Deleted 2 record(s) from collection 'notes' "
                "where file_name=play.txt.\n",
            )

    def test_invalid_delete_filter_keeps_user_facing_error(self) -> None:
        result = _invoke(["delete", "notes", "--where", "file_name"])

        self.assertEqual(result.exit_code, 1)
        self.assertEqual(
            result.stdout,
            "Invalid --where value. Expected <condition>=<value>.\n",
        )

    def test_delete_requires_where_option(self) -> None:
        result = _invoke(["delete", "notes"])

        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("Missing option", result.output)


def _invoke(arguments: Sequence[str]) -> Result:
    return CliRunner().invoke(app, list(arguments))


if __name__ == "__main__":
    unittest.main()
