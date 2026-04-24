# Repository Guidelines

## Project Structure & Module Organization

`chromy/` contains the Python package and CLI implementation. The entrypoint is `chromy/main.py`, which loads environment variables and invokes the Typer app defined in `chromy/cli.py`. The active CLI commands are `list-collections`, `create-collection`, `delete-collection`, `count`, `import`, `query`, and `delete`. Command-specific behavior belongs in `chromy/handlers/`. Shared Chroma, embedding, chunking, querying, and output helpers live in package modules such as `chroma_functions.py`, `embed.py`, `chunk_functions.py`, and `utilities.py`.

`tests/` contains the test suite for the CLI, handlers, and embedding helpers. `README.md` documents user-facing behavior, `pyproject.toml` defines packaging and tool configuration, and `romeo_and_juliet.txt` is a checked-in sample input used by tests and manual CLI runs. Treat generated or local-state directories such as `chroma/`, `dist/`, `chromy.egg-info/`, `.pytest_cache/`, `.mypy_cache/`, `.ruff_cache/`, `.venv/`, `__pycache__/`, and `main.onefile-build/` as non-source. The top-level `handlers/` directory currently contains only legacy bytecode artifacts and should not be treated as source.

## Build, Test, and Development Commands

- `uv sync`: install runtime and development dependencies from `pyproject.toml` and `uv.lock`.
- `uv run python -m chromy.main --help`: run the CLI from the source tree.
- `uv run chromy --help`: run the packaged console script inside the project environment.
- `uv run pytest -q`: run the test suite.
- `uv run ruff check .`: run lint checks.
- `uv run ruff format --check .`: verify formatting.
- `uv run mypy .`: run static type checks.
- `uv build`: build the source distribution and wheel into `dist/`.
- `uv tool install --editable .`: install the `chromy` command in editable mode for local CLI testing.

## Coding Style & Naming Conventions

Use Python 3.12+ syntax, type hints, and `from __future__ import annotations`. Follow the current style: 4-space indentation, snake_case functions and modules, PascalCase classes, and Typer command functions in `chromy/cli.py` that delegate to small handler functions. Keep handlers focused on CLI orchestration and user-facing output; place reusable database, chunking, embedding, query, and formatting logic in shared modules. Prefer `rich` output for user-facing CLI messages to stay consistent with the existing commands.

## Testing Guidelines

Tests run with pytest and are currently written in `unittest.TestCase` style. Name test files `test_*.py` and test methods `test_*`. Prefer mocking Chroma-facing and filesystem-facing functions in CLI and handler tests so unit tests stay deterministic. Run `uv run pytest -q` before submitting changes, and use `uv run ruff check .` plus `uv run mypy .` when touching typed code or shared modules. Add tests for new commands, Typer wiring, handlers, and error paths.

## Security & Configuration Tips

The CLI loads environment variables via `python-dotenv`; keep secrets in local `.env` files and do not commit them. Treat `chroma/` as local persistent database state created by `chromadb.PersistentClient()`. Avoid committing generated build artifacts, cache directories, onefile build outputs, or large ad hoc input files unless they are intentional fixtures. If you change command names or examples, update both `README.md` and the tests so the documented CLI stays aligned with the implementation.
