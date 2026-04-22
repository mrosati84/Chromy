# 7. Modernize Type Hints and Add Missing Future Imports

## Summary

Make type annotations consistent across the codebase by using modern Python 3.12 typing syntax and adding future annotations imports where useful.

## Implementation Steps

- Add `from __future__ import annotations` consistently to Python modules that do not already have it.
- Replace `typing.List` with built-in generic syntax such as `list[str]` and `list[EmbeddingRecord]`.
- Use `collections.abc` input interfaces such as `Sequence[str]` where mutation is not required.
- Introduce type aliases or dataclasses for internal Chroma result shapes only where they reduce ambiguity.
- Keep runtime behavior unchanged.

## Public Interface Changes

- No CLI behavior changes.
- Public Python annotations become more precise and consistent.

## Test Plan

- Run `uv run ruff check .`.
- Run `uv run mypy .` after mypy configuration exists.
- Manually smoke test CLI commands that touched type boundaries.

## Assumptions

- The project remains Python 3.12+, so built-in generic syntax is acceptable everywhere.
- Larger domain model changes should be handled in the service/repository and query-formatting plans.
