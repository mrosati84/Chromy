from __future__ import annotations

from collections.abc import Mapping, Sequence

from chromadb import QueryResult
from rich.console import Console
from rich.rule import Rule
from rich.text import Text

from chromy.chroma_functions import add_data, query_data
from chromy.chunk_functions import chunk_file
from chromy.embed import embed

CONSOLE = Console()


def print_lines(lines: Sequence[str]) -> None:
    for line in lines:
        CONSOLE.print(line)


def ingest_file(collection_name: str, file_path: str) -> int:
    chunks = chunk_file(file_path)
    embeddings = embed(chunks)
    add_data(collection_name, embeddings, file_path)
    return len(embeddings)


def run_query(collection_name: str, query_text: str) -> QueryResult:
    return query_data(collection_name, [query_text])


def format_query_result(result: QueryResult) -> list[Rule | Text]:
    ids = result.get("ids", [[]])
    documents = result.get("documents", [[]])
    distances = result.get("distances", [[]])
    metadatas = result.get("metadatas", [[]])

    first_ids = ids[0] if ids else []
    first_documents = documents[0] if documents else []
    first_distances = distances[0] if distances else []
    first_metadatas = metadatas[0] if metadatas else []

    if not first_ids:
        return [Text.from_markup("[yellow]No results found.[/]")]

    lines: list[Rule | Text] = [Rule(title="Query results")]

    for index, document_id in enumerate(first_ids, start=1):
        lines.append(
            Text.from_markup(f"[bold]{index}[/].\t[green]id[/]\t\t{document_id}")
        )
        i = index - 1

        if i < len(first_distances):
            lines.append(
                Text.from_markup(f"\t[green]distance[/]\t{first_distances[i]}")
            )

        if i < len(first_metadatas):
            metadata = first_metadatas[i]

            if isinstance(metadata, Mapping):
                file_name = metadata.get("file_name")

                if file_name:
                    lines.append(
                        Text.from_markup(f"\t[green]file_name[/]\t{file_name}")
                    )

        if i < len(first_documents):
            lines.append(Text.from_markup("\n[bold green]Retrieved contents[/]\n"))
            lines.append(Text(first_documents[i]))

        # Print a separator between documents
        lines.append(Rule())

    return lines
