from __future__ import annotations

from pathlib import Path
from typing import cast

from semchunk import semchunk

from chromy.embedding import embedding_budget_tokens


def chunk_text(text: str, chunk_size: int | None = None) -> list[str]:
    """
    Split ``text`` into semantically meaningful chunks.

    Args:
        text (str): The text to split.
        chunk_size (int | None): Maximum tokens per chunk, as measured by
            tiktoken. Defaults to ``None``, in which case the active
            embedder's token budget is used.

    Returns:
        list[str]: The resulting chunks.
    """

    if chunk_size is None:
        chunk_size = embedding_budget_tokens()

    chunker = semchunk.chunkerify("gpt-4", chunk_size)
    chunks = chunker(text)

    return cast("list[str]", chunks)


def chunk_file(filename: str, chunk_size: int | None = None) -> list[str]:
    """
    Read and chunk the file at ``filename``.

    Args:
        filename (str): Path to the file to chunk.
        chunk_size (int | None): Maximum tokens per chunk, as measured by
            tiktoken. Defaults to ``None``, in which case the active
            embedder's token budget is used.

    Returns:
        list[str]: The resulting chunks.
    """

    contents = Path(filename).read_text()

    return chunk_text(contents, chunk_size)
