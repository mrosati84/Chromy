# 16. Add Logging for Debuggability

## Summary

Add optional diagnostic logging for ingestion, query, and Chroma operations while keeping normal CLI output clean.

## Implementation Steps

- Configure Python's `logging` module in the CLI entrypoint.
- Add a global `--verbose` flag to enable debug-level logs.
- Log file loading, chunk counts, embedding calls, Chroma writes, collection operations, and query timing.
- Send logs to stderr so stdout remains reserved for command output.
- Avoid logging document contents or full embeddings.

## Public Interface Changes

- Add global CLI flag `--verbose`.
- Normal output remains unchanged when verbose mode is not enabled.

## Test Plan

- Test parser behavior for `--verbose`.
- Test that debug logs are suppressed by default.
- Test that verbose mode emits representative diagnostic logs to stderr.
- Smoke test `add-data` and `query` with verbose mode enabled.

## Assumptions

- A single global verbosity level is enough for now.
- Structured logging means consistent logger names and message fields, not a JSON logging format.
