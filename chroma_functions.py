from typing import List
from uuid import uuid4

import chromadb
from chromadb.api import ClientAPI
from chromadb.api.types import QueryResult
from chromadb.errors import NotFoundError

from embed import EmbeddingRecord


def _get_client_and_collection(
    collection_name: str,
) -> tuple[ClientAPI, chromadb.Collection]:
    client = chromadb.PersistentClient()

    try:
        collection = client.get_collection(name=collection_name)
    except NotFoundError:
        raise

    return client, collection


def list_collections() -> List[str]:
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
    result = collection.delete(where=where)

    return int(result.get("deleted", 0))


def count_collection(collection_name: str) -> int:
    _, collection = _get_client_and_collection(collection_name)

    return collection.count()


def add_data(collection_name: str, data: List[EmbeddingRecord], file_name: str) -> None:
    if not data:
        return

    _, collection = _get_client_and_collection(collection_name)

    collection.add(
        ids=[str(uuid4()) for _ in data],
        metadatas=[{"file_name": file_name} for _ in data],
        documents=[record["text"] for record in data],
        embeddings=[record["embedding"] for record in data],
    )


def query_data(collection_name: str, texts: list[str]) -> QueryResult:
    if not texts:
        return {
            "ids": [],
            "documents": [],
            "metadatas": [],
            "distances": [],
            "embeddings": [],
        }

    _, collection = _get_client_and_collection(collection_name)

    return collection.query(query_texts=texts)
