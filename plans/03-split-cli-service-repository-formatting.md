# 3. Split CLI, Service, Repository, and Formatting Responsibilities

## Summary

Separate command handling, business workflows, Chroma persistence, and output formatting so each layer has a single responsibility.

## Implementation Steps

- Keep handlers thin: receive typed command input, call a service, and print formatted output.
- Move ingestion orchestration from `utilities.ingest_file` into an `IngestionService`.
- Move query orchestration from `utilities.run_query` into a `QueryService`.
- Move Chroma collection operations from `chroma_functions.py` into a `ChromaRepository` or `ChromaStore`.
- Move output-only functions such as `format_query_result` and `print_lines` into a formatting module.
- Keep Chroma-specific result parsing out of CLI handlers.

## Public Interface Changes

- CLI behavior remains unchanged.
- Internal APIs become service and repository methods instead of free functions.
- Formatting functions should accept internal domain objects rather than raw Chroma response dictionaries where possible.

## Test Plan

- Unit test services with mocked repository, chunker, and embedder dependencies.
- Unit test formatter output without requiring Chroma.
- Run a small manual CLI smoke test for create, add, query, count, list, and delete.

## Assumptions

- This should be done after typed command inputs and package layout changes, or coordinated carefully with them.
- No JSON output mode or web API is added in this refactor; the goal is to make those future changes easier.
