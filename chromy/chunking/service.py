from __future__ import annotations

from pathlib import Path
from typing import cast

from semchunk import semchunk


def chunk_text(text: str, chunk_size: int = 800) -> list[str]:
    chunker = semchunk.chunkerify("gpt-4", chunk_size)
    chunks = chunker(text)

    return cast("list[str]", chunks)


def chunk_file(filename: str, chunk_size: int = 800) -> list[str]:
    contents = Path(filename).read_text()

    return chunk_text(contents, chunk_size)
