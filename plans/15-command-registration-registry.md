# 15. Improve Command Registration So Parser and Dispatcher Cannot Drift

## Summary

Unify command parser metadata, handlers, aliases, and error mappings into one registry or add a startup check that prevents parser and dispatcher drift.

## Implementation Steps

- Create one command registry that includes command name, aliases, help text, arguments, handler, and expected error mappings.
- Build argparse subcommands from the registry.
- Dispatch commands through the same registry.
- Remove duplicated command declarations from separate parser and app structures.
- Add a small validation check that command names are unique and aliases do not collide.

## Public Interface Changes

- CLI command names, aliases, arguments, and help text should remain the same.
- Internal command registration becomes centralized.

## Test Plan

- Test that every registry command appears in parser help.
- Test every alias dispatches to the canonical command.
- Test duplicate command or alias validation fails fast.
- Smoke test all existing commands through parser and dispatcher.

## Assumptions

- A unified registry is preferred over only adding a drift-detection test because the current repo already has structured command metadata.
