# 13. Make Query Result Formatting More Robust

## Summary

Convert raw Chroma query results into typed internal matches before formatting them for terminal output.

## Implementation Steps

- Add a `QueryMatch` dataclass with fields for id, document, distance, and metadata.
- Add a parser that converts Chroma `QueryResult` data into `list[QueryMatch]`.
- Handle empty results, missing documents, missing metadata, missing distances, and unexpected metadata shapes defensively.
- Change terminal formatting to accept `list[QueryMatch]`.
- Keep current text output as stable as practical.

## Public Interface Changes

- CLI output should remain effectively the same for normal query results.
- Internal formatter APIs change from raw Chroma result dictionaries to typed match objects.

## Test Plan

- Test empty query results.
- Test populated results with ids, documents, distances, and metadata.
- Test missing documents, missing metadata, multiple query result groups, and non-mapping metadata values.
- Smoke test `query` against a real collection.

## Assumptions

- The first implementation can format the first query group only, matching current behavior.
- Support for alternate output formats is not added in this plan.
