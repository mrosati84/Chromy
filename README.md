# chroma

A small command-line utility for working with a local Chroma database. It lets you create collections, ingest file contents as chunked embeddings, and run similarity queries against stored documents.

## What it does

- manages local Chroma collections
- chunks files with `semchunk`
- generates embeddings with Chroma's default embedding function
- stores chunk text plus source file metadata
- queries collections and prints readable results

## Requirements

- Python 3.12+
- a local environment able to install the project dependencies in `pyproject.toml`

## Installation

Using `uv`:

```bash
uv sync
```

Or with pip:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Running the CLI

The project entrypoint is `main.py`.

```bash
uv run python main.py --help
```

## Commands

```text
list-collections | lc
create-collection | cc <collection>
delete-collection | dc <collection>
count | co <collection>
add-data | ad <collection> <file>
query | q <collection> <query_text>
```

### Examples

Create a collection:

```bash
uv run python main.py create-collection notes
```

Add a file:

```bash
uv run python main.py add-data notes ./docs/example.txt
```

Count stored records:

```bash
uv run python main.py count notes
```

Search the collection:

```bash
uv run python main.py query notes "How do I configure this project?"
```

List collections:

```bash
uv run python main.py list-collections
```

Delete a collection:

```bash
uv run python main.py delete-collection notes
```

## How ingestion works

When you run `add-data`, the file is:

1. read from disk
2. split into chunks
3. embedded
4. inserted into the target collection with the original file path stored as metadata

Query results include the stored document chunk, its id, distance, and file name when available.

## Notes

- collections are stored in a local persistent Chroma database
- `add-data` requires the target collection to already exist
- the CLI prints friendly messages for common errors such as missing collections or missing files
