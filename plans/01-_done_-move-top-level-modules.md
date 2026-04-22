# 1. Move Top-Level Modules Into a Real Package [DONE]

## Summary

Move the current flat module layout into a proper `chromy/` package so imports, packaging, and future subpackages are easier to manage.

## Implementation Steps

- Create a `chromy/` package with `__init__.py`.
- Move `main.py`, `cli_app.py`, `cli_parser.py`, `chroma_functions.py`, `chunk_functions.py`, `embed.py`, and `utilities.py` into `chromy/`.
- Move `handlers/` into `chromy/handlers/`.
- Update imports to absolute package imports such as `from chromy.cli_app import execute_command` and `from chromy.handlers.add_data import handle_add_data`.
- Update `[project.scripts]` in `pyproject.toml` from `main:main` to `chromy.main:main`.
- Update setuptools configuration to package `chromy` and `chromy.handlers` instead of using top-level `py-modules`.
- Update README development commands from `uv run python main.py --help` to `uv run python -m chromy.main --help`.

## Public Interface Changes

- The installed CLI command remains `chromy`.
- Programmatic imports move from top-level modules to `chromy.*`.
- Running from source should use `python -m chromy.main`.

## Test Plan

- Run `uv run python -m chromy.main --help`.
- Run `uv run python -m chromy.main list-collections`.
- Build the package with `uv build`.
- Install locally in editable mode and confirm `chromy --help` resolves the packaged entrypoint.
- Test all commands to verify they still work:
  - [creating, listing, deleting] collections
  - [adding, deleting] documents to a collection (use [romeo_and_juliet.txt](romeo_and_juliet.txt))
  - querying

## Assumptions

- Backward-compatible top-level imports are not required.
- The package refactor should preserve behavior before deeper service or architecture changes are made.
