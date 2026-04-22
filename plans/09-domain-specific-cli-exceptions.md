# 9. Use Domain-Specific Exceptions Instead of Chroma Exceptions in CLI Mapping

## Summary

Hide Chroma-specific exceptions behind application-level exceptions so the CLI does not depend on Chroma's exception model.

## Implementation Steps

- Define app-level exceptions such as `CollectionNotFoundError`, `CollectionAlreadyExistsError`, and `StorageOperationError`.
- Convert Chroma exceptions inside the repository layer.
- Update CLI command error mappings to handle app-level exceptions only.
- Preserve existing user-facing messages for missing and duplicate collections.
- Avoid importing `chromadb.errors` in CLI modules after the repository layer owns that boundary.

## Public Interface Changes

- CLI behavior and messages should remain the same.
- Internal error contracts change from Chroma exceptions to app-level exceptions.

## Test Plan

- Unit test repository exception translation.
- Unit test CLI mappings for app-level exceptions.
- Smoke test missing collection, duplicate collection, and successful operations.

## Assumptions

- Chroma remains the only storage backend for now.
- The exception layer is still useful because it prevents storage details from leaking upward.
