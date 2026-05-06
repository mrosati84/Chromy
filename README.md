# Chromy

<div align="center">
    <img src="logo.png" width=300 />
</div>

Chromy is small and simple to use command-line utility for working with a local Chroma database. It lets you create collections, ingest files as chunked embeddings, and run similarity queries against stored documents. It integrates perfectly with agentic coding tools via simple skills (see an [example](./skills/chromy/SKILL.md) in the `skills` directory).

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

## Chroma storage location

By default, Chromy uses Chroma's default persistent location behavior (a local
`chroma/` directory based on your current working directory when you run the
command).

You can override this with `CHROMA_FOLDER`.

- `CHROMA_FOLDER` must point to a **parent directory**.
- Chromy will store data in `<CHROMA_FOLDER>/chroma`.
- Relative paths are supported and are resolved from the current working directory.
- If `CHROMA_FOLDER` is set, it takes precedence over the default behavior.
- If the configured location is invalid or not writable, the command fails with an explicit error (no fallback to the default location).

Examples:

```bash
# absolute parent path
CHROMA_FOLDER=/tmp/chromy-data chromy list-collections

# relative parent path (resolved from current directory)
CHROMA_FOLDER=.local-data chromy create-collection notes
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
list-collections
create-collection <collection>
delete-collection <collection>
count <collection>
import <collection> <file> [<file> ...]
query <collection> <query_text>
delete <collection> --where <condition>=<value>
```

### Examples

Create a collection:

```bash
chromy create-collection notes
```

Add one or more files:

```bash
chromy import notes ./docs/example.txt
chromy import notes ./docs/intro.md ./docs/setup.md
chromy import notes *.md
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

Delete records by metadata:

```bash
chromy delete notes --where file_name=example.txt
```

## How ingestion works

When you run `import`, each file is:

1. read from disk
2. split into chunks
3. embedded
4. inserted into the target collection with the original file path stored as metadata

Query results include the stored document chunk, its id, distance, and file name when available.

## Notes

- by default, collections are stored in a local persistent Chroma database in the current directory
- set `CHROMA_FOLDER` to override the parent location; Chromy will use `<CHROMA_FOLDER>/chroma`
- `import` requires the target collection to already exist
- `import` accepts one or more file paths
- unquoted glob patterns such as `*.md` are expanded by the shell before `chromy` starts
- quoted glob patterns such as `"*.md"` are treated as literal paths and are not expanded by `chromy`
- unmatched unquoted globs may behave differently by shell: `zsh` commonly fails before `chromy` starts, while `bash` may pass the literal pattern through depending on shell settings
- the CLI reports file-specific import failures and continues with the remaining files
- when importing multiple files in an interactive terminal, the CLI shows a Rich progress bar
