# 14. Clarify Delete Filter Semantics

## Summary

Make it clear that record deletion supports a simple metadata equality filter in `key=value` form.

## Implementation Steps

- Rename internal parser variables from `condition` to `key` where equality-only semantics are intended.
- Update CLI help for `--where` to say `Metadata equality filter in the format <key>=<value>`.
- Update error messages to use `<key>=<value>`.
- Update README command documentation to include the `delete` command and its filter syntax.
- Reserve richer Chroma filters, such as JSON filters, for a later feature.

## Public Interface Changes

- CLI option remains `--where`.
- Help text and error messages become more precise.
- No richer filter syntax is added yet.

## Test Plan

- Test valid `key=value` parsing with whitespace trimming.
- Test missing separator, empty key, and empty value errors.
- Verify `chromy delete --help` documents equality semantics.

## Assumptions

- Keeping the option name `--where` is acceptable for backward compatibility.
- Renaming to `--key` is not worth the CLI break for the current feature set.
