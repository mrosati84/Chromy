from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from chromy.chroma_functions import get_client
from chromy.errors import ChromaPathError


class ChromaFunctionsTests(unittest.TestCase):
    def test_get_client_uses_default_when_env_is_unset(self) -> None:
        with (
            patch.dict(os.environ, {}, clear=True),
            patch("chromy.chroma_functions.chromadb.PersistentClient") as persistent,
        ):
            get_client()

        persistent.assert_called_once_with()

    def test_get_client_uses_chroma_folder_override(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            configured_parent = Path(temp_dir) / "data"

            with (
                patch.dict(os.environ, {"CHROMA_FOLDER": str(configured_parent)}),
                patch(
                    "chromy.chroma_functions.chromadb.PersistentClient"
                ) as persistent,
            ):
                get_client()

            expected_path = configured_parent.resolve() / "chroma"
            persistent.assert_called_once_with(path=str(expected_path))
            self.assertTrue(expected_path.is_dir())

    def test_get_client_resolves_relative_chroma_folder_from_cwd(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            working_dir = Path(temp_dir)
            previous_cwd = Path.cwd()

            try:
                os.chdir(working_dir)
                with (
                    patch.dict(os.environ, {"CHROMA_FOLDER": "relative-parent"}),
                    patch(
                        "chromy.chroma_functions.chromadb.PersistentClient"
                    ) as persistent,
                ):
                    get_client()
            finally:
                os.chdir(previous_cwd)

            expected_path = (working_dir / "relative-parent").resolve() / "chroma"
            persistent.assert_called_once_with(path=str(expected_path))

    def test_get_client_fails_when_configured_path_is_not_usable(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            invalid_parent = Path(temp_dir) / "not-a-directory"
            invalid_parent.write_text("x", encoding="utf-8")

            with (
                patch.dict(os.environ, {"CHROMA_FOLDER": str(invalid_parent)}),
                self.assertRaisesRegex(
                    ChromaPathError,
                    "Could not create or access Chroma directory",
                ),
            ):
                get_client()

    def test_get_client_wraps_client_initialization_failures(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            configured_parent = Path(temp_dir)

            with (
                patch.dict(os.environ, {"CHROMA_FOLDER": str(configured_parent)}),
                patch(
                    "chromy.chroma_functions.chromadb.PersistentClient",
                    side_effect=RuntimeError("boom"),
                ),
                self.assertRaisesRegex(
                    ChromaPathError,
                    "Could not initialize Chroma client",
                ),
            ):
                get_client()


if __name__ == "__main__":
    unittest.main()
