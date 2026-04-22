# Repository Guidelines

## Project Structure & Module Organization

`chromy/` contains the Python package and CLI implementation. The entrypoint is `chromy/main.py`, parser wiring is in `chromy/cli_parser.py`, command dispatch is in `chromy/cli_app.py`, and typed command inputs live in `chromy/command_inputs.py`. Command-specific behavior belongs in `chromy/handlers/`. Shared Chroma, embedding, chunking, and formatting helpers live in package modules such as `chroma_functions.py`, `embed.py`, `chunk_functions.py`, and `utilities.py`.

`tests/` contains the pytest suite. `plans/` holds planning notes. Generated data and build outputs such as `chroma/`, `dist/`, `chromy.egg-info/`, caches, and `.venv/` are not source.

## Build, Test, and Development Commands

- `uv sync`: install runtime and development dependencies from `pyproject.toml` and `uv.lock`.
- `uv run python -m chromy.main --help`: run the CLI from the source tree.
- `uv run pytest -q`: run the test suite.
- `uv build`: build the source distribution and wheel into `dist/`.
- `uv tool install --editable .`: install the `chromy` command in editable mode for local CLI testing.

## Coding Style & Naming Conventions

Use Python 3.12+ syntax, type hints, and `from __future__ import annotations`. Follow the current style: 4-space indentation, snake_case functions and modules, PascalCase dataclasses/classes, and explicit command input objects instead of raw `argparse.Namespace` in handlers. Keep handlers focused on CLI orchestration; place reusable database or formatting logic in shared modules.

## Testing Guidelines

Tests use pytest and currently include `unittest.TestCase`-style cases. Name test files `test_*.py` and test methods `test_*`. Prefer mocking Chroma-facing functions in handler tests so unit tests stay deterministic. Run `uv run pytest -q` before submitting changes, and add tests for new commands, parser behavior, handlers, and error paths.

## Commit & Pull Request Guidelines

Git history uses short, imperative, lowercase commit subjects, for example `move top-level modules into a real package` and `replace argparse.Namespace plumbing with typed command inputs`. Keep commits scoped to one logical change.

Pull requests should include a concise description, test results, and notes for any CLI behavior changes. Link related issues or plan files when applicable. Include terminal output examples or screenshots only when user-facing command output changes.

## Security & Configuration Tips

The CLI loads environment variables via `python-dotenv`; keep secrets in local `.env` files and do not commit them. Treat `chroma/` as local persistent database state. Avoid committing generated build artifacts, cache directories, or large ad hoc input files unless they are intentional fixtures.
