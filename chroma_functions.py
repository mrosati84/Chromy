import chromadb
from typing import List


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
    # TODO Implement this method.
    # The function must use the count method and return how many records are
    # in the collection. It must handle non-existent collections.
    raise NotImplemented()
