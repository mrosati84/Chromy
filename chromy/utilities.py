from __future__ import annotations

from pathlib import Path

from chromadb import QueryResult

from chromy.chroma_functions import add_data, delete_data, has_data_for_file, query_data
from chromy.chunk_functions import chunk_file
from chromy.embed import embed


def ingest_file(collection_name: str, file_path: str) -> int:
    if has_data_for_file(collection_name, file_path):
        delete_data(collection_name, {"file_name": file_path})

    chunks = chunk_file(file_path)
    embeddings = embed(chunks)
    add_data(collection_name, embeddings, file_path)
    return len(embeddings)


def run_query(collection_name: str, query_text: str) -> QueryResult:
    return query_data(collection_name, [query_text])


def is_probably_text_file(path: str | Path, sample_size: int = 8192) -> bool:
    """
    Return whether a file appears to contain text.

    Args:
        path (str | Path): The path to the file to inspect.
        sample_size (int): The maximum number of bytes to read from the file.

    Returns:
        bool: ``True`` if the sampled bytes decode as UTF-8, UTF-8 with BOM,
        UTF-16, or UTF-32, or if the file is empty. Otherwise, ``False``.
    """

    path = Path(path)

    with path.open("rb") as f:
        sample = f.read(sample_size)

    if not sample:
        return True

    encodings = (
        "utf-8",
        "utf-8-sig",
        "utf-16",
        "utf-32",
    )

    for encoding in encodings:
        try:
            sample.decode(encoding)
            return True
        except UnicodeDecodeError:
            pass

    return False
