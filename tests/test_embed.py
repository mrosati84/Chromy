from __future__ import annotations

import unittest
from unittest.mock import patch

from chromadb.utils.embedding_functions import DefaultEmbeddingFunction

from chromy.embedding import MODEL_HEADROOM, embed, embedding_budget_tokens


class EmbedTest(unittest.TestCase):
    def test_embed_returns_empty_list_for_empty_chunks(self) -> None:
        self.assertEqual(embed([]), [])

    def test_embedding_budget_tokens_scales_max_tokens_by_headroom(self) -> None:
        self.assertEqual(
            embedding_budget_tokens(),
            max(1, int(DefaultEmbeddingFunction().max_tokens() * MODEL_HEADROOM)),
        )

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
