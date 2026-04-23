from __future__ import annotations

import unittest
from collections.abc import Sequence
from pathlib import Path
from unittest.mock import patch

from chromadb.errors import InternalError
from click.testing import Result
from typer.testing import CliRunner

from chromy.cli import app


class CliTests(unittest.TestCase):
    @staticmethod
    def _fixture_path(path: str) -> str:
        return str(Path(path).resolve())

    def test_list_empty_collections(self) -> None:
        with patch(
            "chromy.handlers.list_collections.list_collections",
            return_value=[],
        ):
            result = _invoke(["list-collections"])

        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.stdout, "No collections found.\n")

    def test_list_existing_collections(self) -> None:
        with patch(
            "chromy.handlers.list_collections.list_collections",
            return_value=["books", "code"],
        ):
            result = _invoke(["list-collections"])

        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.stdout, "books\ncode\n")

    def test_create_collection(self) -> None:
        with patch(
            "chromy.handlers.create_collection.create_collection",
            return_value="notes",
        ) as create_collection:
            result = _invoke(["create-collection", "notes"])

        create_collection.assert_called_once_with("notes")
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.stdout, "Created collection 'notes'.\n")

    def test_create_collection_with_same_name(self) -> None:
        with patch(
            "chromy.handlers.create_collection.create_collection",
            side_effect=InternalError()

        ) as create_collection:
            result = _invoke(["create-collection", "notes"])

        create_collection.assert_called_once_with("notes")
        self.assertEqual(result.exit_code, 1)
        self.assertEqual(result.stdout, "Collection 'notes' already exists.\n")

    def test_delete_collection(self) -> None:
        with patch(
            "chromy.handlers.delete_collection.delete_collection",
        ) as delete_collection:
            result = _invoke(["delete-collection", "notes"])

        delete_collection.assert_called_once_with("notes")
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.stdout, "Deleted collection 'notes'.\n")

    def test_count(self) -> None:
        with patch(
            "chromy.handlers.count_collection.count_collection",
            return_value=7,
        ) as count_collection:
            result = _invoke(["count", "notes"])

        count_collection.assert_called_once_with("notes")
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.stdout, "7\n")

    def test_import_data(self) -> None:
        with patch(
            "chromy.handlers.import_data.ingest_file",
            return_value=3,
        ) as ingest_file:
            result = _invoke(["import", "notes", "romeo_and_juliet.txt"])

        ingest_file.assert_called_once_with(
            "notes",
            self._fixture_path("romeo_and_juliet.txt"),
        )
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(
            result.stdout, "Added 3 records to collection 'notes'.\n")

    def test_query(self) -> None:
        query_result = {"ids": [["1"]], "documents": [["hello"]]}

        with (
            patch("chromy.handlers.query.run_query", return_value=query_result) as run,
            patch(
                "chromy.handlers.query.format_query_result",
                return_value=["Query results:", "1"],
            ) as format_result,
        ):
            result = _invoke(["query", "notes", "Where is Romeo?"])

        run.assert_called_once_with("notes", "Where is Romeo?")
        format_result.assert_called_once_with(query_result)
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.stdout, "Query results:\n1\n")

    def test_delete_records(self) -> None:
        with patch(
            "chromy.handlers.delete_collection.delete_data",
            return_value=2,
        ) as delete_data:
            result = _invoke(
                ["delete", "notes", "--where", " file_name = play.txt "],
            )

        delete_data.assert_called_once_with("notes", {"file_name": "play.txt"})
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(
            result.stdout,
            "Deleted 2 record(s) from collection 'notes' "
            "where file_name=play.txt.\n",
        )

    def test_removed_alias_is_rejected(self) -> None:
        result = _invoke(["lc"])

        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("No such command", result.output)

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
