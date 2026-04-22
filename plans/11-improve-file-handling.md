# 11. Improve File Handling

## Summary

Make file ingestion boundaries clearer by using `Path`, explicit UTF-8 decoding, and validation before reading.

## Implementation Steps

- Change internal file ingestion APIs to accept `Path` instead of raw `str`.
- Convert CLI string paths to `Path` in the command adapter or handler.
- Validate that the path exists and is a regular file before reading.
- Read text with `encoding="utf-8"`.
- Raise a clear app-level file error for missing paths, directories, and decoding failures.
- Leave PDF and future file loaders out of scope for now.

## Public Interface Changes

- CLI argument remains a file path string.
- Error messages for missing or invalid files become clearer.

## Test Plan

- Test successful text-file loading.
- Test missing file, directory path, and invalid UTF-8 handling.
- Smoke test `add-data` with a valid UTF-8 file.

## Assumptions

- Only plain text ingestion is supported in this plan.
- Existing metadata can continue storing the original path string as `file_name` unless a later plan changes metadata shape.
