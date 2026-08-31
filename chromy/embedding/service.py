from __future__ import annotations

from collections.abc import Sequence
from typing import Final, TypedDict

from chromadb.utils.embedding_functions import DefaultEmbeddingFunction

# semchunk counts tokens with tiktoken, which differs from the embedder's own
# (wordpiece) tokenizer. The headroom keeps real token counts under the
# embedder's input limit despite that counting skew.
MODEL_HEADROOM: Final = 0.8


class EmbeddingRecord(TypedDict):
    text: str
    embedding: list[float]


def embedding_budget_tokens() -> int:
    """
    Return the per-chunk token budget for the active embedder.

    Scales the embedder's maximum input length by ``MODEL_HEADROOM`` so that
    tiktoken-measured chunks stay within the embedder's actual token limit.

    Returns:
        int: Maximum number of (tiktoken-counted) tokens per chunk.
    """

    max_tokens = DefaultEmbeddingFunction().max_tokens()
    return max(1, int(max_tokens * MODEL_HEADROOM))


def embed(chunks: Sequence[str]) -> list[EmbeddingRecord]:
    if not chunks:
        return []

    embedding_function = DefaultEmbeddingFunction()
    embeddings = embedding_function(list(chunks))

    return [
        {
            "text": text,
            "embedding": (
                embedding.tolist() if hasattr(embedding, "tolist") else list(embedding)
            ),
        }
        for text, embedding in zip(chunks, embeddings, strict=False)
    ]
