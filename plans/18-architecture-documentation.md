# 18. Add Repository-Level Documentation for Architecture

## Summary

Document the intended internal architecture so future changes follow the same parser, handler, service, repository, and formatter boundaries.

## Implementation Steps

- Add a "Development Architecture" section to README or create `docs/architecture.md`.
- Describe the request flow: CLI parser -> command input -> handler -> service -> Chroma repository -> formatter.
- Explain where to add a new command.
- Explain where to add a new document loader.
- Explain where to add a new embedding provider.
- Include the default Chroma persistence behavior and how configuration is injected after that refactor exists.

## Public Interface Changes

- No runtime behavior changes.
- Developer-facing documentation is added or expanded.

## Test Plan

- Verify documentation matches the actual package/module layout after refactors.
- Run README examples to ensure commands are still accurate.
- Check links and command snippets manually.

## Assumptions

- Documentation should be updated after or alongside the architecture refactor so it describes the intended final shape.
- A README section is enough unless the architecture content grows too large.
