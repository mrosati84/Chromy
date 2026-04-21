import chromadb
from chromadb.errors import NotFoundError
from typing import List
from uuid import uuid4

from embed import EmbeddingRecord


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


def count_collection(name: str) -> int:
    client = chromadb.PersistentClient()

    try:
        collection = client.get_collection(name=name)
    except NotFoundError:
        raise

    return collection.count()


def add_data(collection: str, data: List[EmbeddingRecord]) -> None:
    if not data:
        return

    client = chromadb.PersistentClient()

    try:
        target_collection = client.get_collection(name=collection)
    except NotFoundError:
        raise

    target_collection.add(
        ids=[str(uuid4()) for _ in data],
        documents=[record["text"] for record in data],
        embeddings=[record["embedding"] for record in data],
    )
