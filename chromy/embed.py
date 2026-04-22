from typing import List, TypedDict

from chromadb.utils.embedding_functions import DefaultEmbeddingFunction


class EmbeddingRecord(TypedDict):
    text: str
    embedding: List[float]


def embed(chunks: List[str]) -> List[EmbeddingRecord]:
    if not chunks:
        return []

    embedding_function = DefaultEmbeddingFunction()
    embeddings = embedding_function(chunks)

    return [
        {
            "text": text,
            "embedding": (
                embedding.tolist() if hasattr(embedding, "tolist") else list(embedding)
            ),
        }
        for text, embedding in zip(chunks, embeddings)
    ]
