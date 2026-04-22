# 8. Avoid Catching `BaseException` in CLI Dispatch

## Summary

Change CLI dispatch error handling so process-control exceptions such as `KeyboardInterrupt` and `SystemExit` are not swallowed.

## Implementation Steps

- Change `execute_command` to catch `Exception` instead of `BaseException`.
- Keep mapped, expected errors handled through the existing command error mapping or its replacement.
- Print handled user-facing errors to `stderr` instead of `stdout`.
- Allow unmapped exceptions, `KeyboardInterrupt`, and `SystemExit` to propagate normally.
- Consider adding debug logging for unexpected exceptions after the logging plan exists.

## Public Interface Changes

- Expected command errors still return a non-zero exit code.
- Handled error messages move from stdout to stderr.
- Interrupt and process-exit behavior becomes conventional.

## Test Plan

- Test that a mapped exception returns `1` and writes to stderr.
- Test that `KeyboardInterrupt` is not caught by `execute_command`.
- Test that unmapped exceptions still propagate.

## Assumptions

- Returning `1` for handled user errors remains acceptable until the exit-code conventions plan is implemented.
