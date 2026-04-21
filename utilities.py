from chromadb import QueryResult

from chroma_functions import add_data, query_data
from chunk_functions import chunk_file
from embed import embed


def print_lines(lines: list[str]) -> None:
    for line in lines:
        print(line)


def ingest_file(collection_name: str, file_path: str) -> int:
    chunks = chunk_file(file_path)
    embeddings = embed(chunks)
    add_data(collection_name, embeddings)
    return len(embeddings)


def run_query(collection_name: str, query_text: str) -> QueryResult:
    return query_data(collection_name, [query_text])


def format_query_result(result: QueryResult) -> list[str]:
    ids = result.get("ids", [[]])
    documents = result.get("documents", [[]])
    distances = result.get("distances", [[]])

    first_ids = ids[0] if ids else []
    first_documents = documents[0] if documents else []
    first_distances = distances[0] if distances else []

    if not first_ids:
        return ["No results found."]

    lines = ["Query results:"]
    for index, document_id in enumerate(first_ids, start=1):
        lines.append(f"{index}. id: {document_id}")

        if index - 1 < len(first_distances):
            lines.append(f"   distance: {first_distances[index - 1]}")

        if index - 1 < len(first_documents):
            lines.append(f"   document: {first_documents[index - 1]}")

    return lines
