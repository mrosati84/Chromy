from pathlib import Path
from typing import List

import semchunk


def chunk_text(text: str, chunk_size: int = 800) -> List[str]:
    chunker = semchunk.chunkerify("gpt-4", chunk_size)
    chunks = chunker(text)

    return chunks


def chunk_file(filename: str, chunk_size: int = 800) -> List[str]:
    contents = Path(filename).read_text()

    return chunk_text(contents, chunk_size)
