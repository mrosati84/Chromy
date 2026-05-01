from __future__ import annotations

from collections.abc import Sequence
from typing import cast
from uuid import uuid4

import chromadb
from chromadb.api import ClientAPI
from chromadb.api.types import QueryResult, Where
from chromadb.errors import NotFoundError

from chromy.embedding import EmbeddingRecord


def _get_client_and_collection(
    collection_name: str,
) -> tuple[ClientAPI, chromadb.Collection]:
    client = chromadb.PersistentClient()

    try:
        collection = client.get_collection(name=collection_name)
    except NotFoundError:
        raise

    return client, collection


def list_collections() -> list[str]:
    client = chromadb.PersistentClient()
    collections = client.list_collections()

    if not collections:
        return []

    return [getattr(collection, "name", str(collection)) for collection in collections]


def create_collection(name: str) -> str:
    client = chromadb.PersistentClient()
    collection = client.create_collection(name=name)

    return getattr(collection, "name", name)


def delete_collection(name: str) -> None:
    client = chromadb.PersistentClient()
    client.delete_collection(name=name)


def delete_data(collection_name: str, where: dict[str, str]) -> int:
    _, collection = _get_client_and_collection(collection_name)
    result = collection.delete(where=cast(Where, where))

    return int(result.get("deleted", 0))


def has_data_for_file(collection_name: str, file_name: str) -> bool:
    _, collection = _get_client_and_collection(collection_name)
    result = collection.get(where=cast(Where, {"file_name": file_name}))
    ids = result.get("ids", [])

    return len(ids) > 0


def count_collection(collection_name: str) -> int:
    _, collection = _get_client_and_collection(collection_name)
    return collection.count()


def add_data(
    collection_name: str,
    data: Sequence[EmbeddingRecord],
    file_name: str,
) -> None:
    if not data:
        return

    _, collection = _get_client_and_collection(collection_name)

    embeddings: list[Sequence[float]] = [record["embedding"] for record in data]

    collection.add(
        ids=[str(uuid4()) for _ in data],
        metadatas=[{"file_name": file_name} for _ in data],
        documents=[record["text"] for record in data],
        embeddings=embeddings,
    )


def query_data(collection_name: str, texts: Sequence[str]) -> QueryResult:
    if not texts:
        return {
            "ids": [],
            "documents": [],
            "metadatas": [],
            "distances": [],
            "embeddings": None,
            "uris": None,
            "data": None,
            "included": ["documents", "metadatas", "distances"],
        }

    _, collection = _get_client_and_collection(collection_name)

    return collection.query(query_texts=list(texts))
