from __future__ import annotations

from collections.abc import Sequence
from typing import TypedDict

from chromadb.utils.embedding_functions import DefaultEmbeddingFunction


class EmbeddingRecord(TypedDict):
    text: str
    embedding: list[float]


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
