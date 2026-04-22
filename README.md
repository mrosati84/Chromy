# Chromy

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

For local development, install the project dependencies with `uv`:

```bash
uv sync
```

Or with pip:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Build

Build the source distribution and wheel with `uv`:

```bash
uv build
```

The build artifacts are written to `dist/`.

## Install as a tool with uv

The project exposes a `chromy` command through the Python packaging entrypoint.
Install it as a standalone `uv` tool from the project directory:

```bash
uv tool install .
```

After installation, run the CLI directly:

```bash
chromy --help
```

To install from a built wheel instead:

```bash
uv build
uv tool install dist/chromy-1.0.0-py3-none-any.whl
```

During development, install the tool in editable mode so changes in the working
tree are picked up without reinstalling:

```bash
uv tool install --editable .
```

## Running the CLI

The project entrypoint is available as the `chromy` command after installing the
tool:

```bash
chromy --help
```

You can also run it from the source tree without installing the tool:

```bash
uv run python -m chromy.main --help
```

## Running Tests

Run the test suite with pytest:

```bash
uv run pytest -q
```

## Development Checks

Run Ruff linting:

```bash
uv run ruff check .
```

Check Ruff formatting:

```bash
uv run ruff format --check .
```

Run static type checking with mypy:

```bash
uv run mypy .
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
chromy create-collection notes
```

Add a file:

```bash
chromy add-data notes ./docs/example.txt
```

Count stored records:

```bash
chromy count notes
```

Search the collection:

```bash
chromy query notes "How do I configure this project?"
```

List collections:

```bash
chromy list-collections
```

Delete a collection:

```bash
chromy delete-collection notes
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
