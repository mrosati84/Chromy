# 4. Centralize Chroma Client Configuration

## Summary

Create Chroma client configuration once per command and inject it into repository or service objects instead of repeatedly calling `chromadb.PersistentClient()`.

## Implementation Steps

- Add a small configuration object for Chroma settings, including persistence path.
- Load the persistence path from a CLI option, environment variable, or default Chroma behavior.
- Create a Chroma client factory that returns one client per command execution.
- Inject the client into the Chroma repository instead of constructing it inside each function.
- Remove repeated `chromadb.PersistentClient()` calls from collection operations.
- Ensure tests can pass an in-memory or temporary Chroma client.

## Public Interface Changes

- Add a documented way to configure the Chroma persistence path.
- Existing commands should continue to work with the current implicit default when no path is provided.

## Test Plan

- Unit test repository operations with an injected test client.
- Verify two commands using the same configured persistence directory can see the same collections.
- Verify default behavior still works when no path is configured.

## Assumptions

- The initial implementation should preserve Chroma's default persistence behavior unless a path is explicitly configured.
- Configuration should be introduced before larger repository and service tests depend on isolated storage.
