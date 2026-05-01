from __future__ import annotations

import unittest
from unittest.mock import patch

from chromy.embedding import embed


class EmbedTest(unittest.TestCase):
    def test_embed_returns_empty_list_for_empty_chunks(self) -> None:
        self.assertEqual(embed([]), [])

    def test_embed_pairs_text_with_list_embeddings(self) -> None:
        with patch(
            "chromy.embedding.service.DefaultEmbeddingFunction",
            return_value=lambda chunks: ((1.0, 2.0), (3.0, 4.0)),
        ):
            result = embed(["first", "second"])

        self.assertEqual(
            result,
            [
                {"text": "first", "embedding": [1.0, 2.0]},
                {"text": "second", "embedding": [3.0, 4.0]},
            ],
        )


if __name__ == "__main__":
    unittest.main()
