# ADR 0001: Migration from Ruby to Python

## Status

Proposed

## Context

The project currently uses Ruby for its core logic. The user requested a migration to Python because Python is more commonly pre-installed on their servers.

## Decision

We will migrate the core logic from Ruby to Python with the following constraints:

1.  **Runtime Environment**: Target Python 3.6+ using only the standard library (no third-party dependencies at runtime).
2.  **Processing Mode**: Use a "dual-mode" approach:
    -   **Logic/Search**: Use `str` (UTF-8) for word matching and index calculation.
    -   **Rendering/UI**: Use `bytes` for writing to the TTY and handling `tmux capture-pane -ep` output to prevent encoding errors with ANSI sequences.
3.  **Concurrency**: Use `threading` and `queue` to replicate the Ruby implementation's input handling and cancellation logic.
4.  **Testing**: Use `pytest` for development/testing (dev dependency allowed).
5.  **Coexistence**: Keep Ruby files (`.rb`, `Gemfile`, `spec/`) during the migration for validation; remove them only after the Python version is verified.

## Consequences

-   **Pros**: Improved portability across servers without Ruby environments.
-   **Cons**: Temporary duplication of logic in the codebase during the migration.
