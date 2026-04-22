# 6. Add Ruff and Mypy Configuration [DONE]

## Summary

Add linting, formatting, and static type checking configuration to `pyproject.toml`. Do not add pytest configuration for this improvement.

## Implementation Steps

- Add `ruff` and `mypy` to the development dependency group.
- Configure Ruff formatting and lint rules in `pyproject.toml`.
- Configure mypy in strict or near-strict mode suitable for the current Chroma and third-party boundaries.
- Add README development commands for `uv run ruff check .`, `uv run ruff format .`, and `uv run mypy .`.
- Fix only minimal configuration blockers in this plan; broad type modernization belongs to the type-hints plan.

## Public Interface Changes

- No runtime CLI behavior changes.
- Development workflow gains standard lint, format, and type-check commands.

## Test Plan

- Run `uv run ruff check .`.
- Run `uv run ruff format --check .`.
- Run `uv run mypy .`.
- Confirm no pytest configuration is added as part of this plan.

## Assumptions

- Pytest is intentionally out of scope for this improvement.
- Strict mypy may need targeted ignores for third-party packages that do not expose complete typing.
