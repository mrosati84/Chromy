# 17. Add Exit Code Conventions

## Summary

Document and implement consistent exit codes so scripts can distinguish success from expected user errors.

## Implementation Steps

- Define named constants or an enum for exit codes.
- Use `0` for success.
- Use `1` for expected user-facing errors initially.
- Optionally reserve distinct documented codes for validation errors, missing collections, and file errors if the CLI needs them.
- Update error handling to return constants instead of literal integers.
- Document exit code behavior in README.

## Public Interface Changes

- Existing successful commands still exit `0`.
- Existing handled errors may continue to exit `1` unless distinct codes are explicitly adopted.
- README documents the convention.

## Test Plan

- Test success returns `0`.
- Test expected user errors return the documented code.
- Test unexpected exceptions still propagate to the runtime.
- Manually verify shell exit status for representative commands.

## Assumptions

- Start with `0` and `1` unless there is a clear automation need for more granular codes.
- This plan should follow the exception cleanup plan so errors are categorized at the app level.
