# 10. Make Ingestion More Configurable

## Summary

Move chunking and embedding choices into configuration and expose chunk size as an `add-data` CLI option.

## Implementation Steps

- Add ingestion configuration for chunk size, tokenizer/model name, and embedding function provider.
- Change chunking code to receive chunk size and tokenizer/model name instead of hard-coding `800` and `"gpt-4"`.
- Reuse the embedding function through dependency injection instead of constructing it for every embed call.
- Add `--chunk-size` to `add-data`, defaulting to the current value of `800`.
- Keep the default tokenizer/model behavior equivalent to the current `"gpt-4"` setting.

## Public Interface Changes

- `add-data` gains `--chunk-size`.
- Default ingestion behavior remains unchanged when no option is provided.

## Test Plan

- Test chunking with default and custom chunk sizes.
- Test `add-data --chunk-size` parser behavior.
- Test ingestion service with an injected fake embedder.
- Smoke test adding a file with and without `--chunk-size`.

## Assumptions

- Only chunk size is exposed in the CLI initially.
- Tokenizer/model and embedding provider configuration can remain internal or environment-backed until there is a concrete user-facing need.
