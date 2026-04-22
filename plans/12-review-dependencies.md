# 12. Review Dependencies and Remove Unused Ones

## Summary

Audit runtime dependencies and move unused or optional packages out of the base install where appropriate.

## Implementation Steps

- Compare imports in source code against dependencies declared in `pyproject.toml`.
- Keep packages that are directly imported by current runtime code.
- Move packages used only for optional or future features behind extras, such as `pdf` or `openai`.
- Remove dependencies that are neither imported nor needed transitively by active code.
- Update `uv.lock` after dependency changes.
- Update README installation notes if extras are introduced.

## Public Interface Changes

- Base installation may become smaller.
- Optional feature dependencies should be installed through extras if introduced.

## Test Plan

- Run `uv sync` after dependency edits.
- Run `uv run python -m chromy.main --help`.
- Smoke test commands that use Chroma, semchunk, dotenv loading, and embedding.
- Build the package with `uv build`.

## Assumptions

- Dependency removal should be conservative and based on actual import usage.
- No new optional features are implemented as part of this cleanup.
