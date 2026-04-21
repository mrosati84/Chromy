from typing import List

import semchunk


def chunk(text: str, chunk_size: int = 800) -> List[str]:
    chunker = semchunk.chunkerify("gpt-4", chunk_size)
    chunks = chunker(text)

    return chunks
