# 2. Replace `argparse.Namespace` Plumbing With Typed Command Inputs

## Summary

Stop passing mutable `argparse.Namespace` objects into handlers. Convert parsed CLI arguments into typed command dataclasses before dispatch.

## Implementation Steps

- Add frozen dataclasses for command inputs, such as list collections, create collection, delete collection, count, add data, query, and delete records.
- Keep `argparse` isolated in the CLI adapter layer.
- Convert `Namespace` into the correct command dataclass immediately before dispatch.
- Change handler signatures from `Callable[[Namespace], int]` to typed command-specific callables.
- Remove mutations such as `args.error_message = ...` in `cli_app.py` and `handlers/delete_collection.py`.
- Return or raise explicit structured results/errors rather than writing temporary state back into the parsed args object.

## Public Interface Changes

- CLI command syntax stays the same.
- Internal handler APIs change to typed dataclass inputs.
- Error message builders should receive typed command inputs or exceptions instead of raw `Namespace`.

## Test Plan

- Add parser-to-command conversion tests for every command and alias.
- Add handler unit tests that construct command dataclasses directly.
- Verify invalid delete filters still produce the same user-facing error.

## Assumptions

- Command dataclasses should live near CLI application code until a broader package refactor introduces clearer subpackages.
- The first pass should preserve the existing command names, arguments, aliases, and output.
