# TASKS.md

## Priority next tasks

1. Add automated tests that lock down current behavior before any semantics change.
2. Refactor `src/exr_checker/cli.py` so validation and sequence logic can be tested without relying on `sys.exit`.
3. Decide whether missing frames should remain informational or become a non-zero exit for pipeline use.
4. Decide whether "no files found" should remain exit `0` or become a warning/failure code.
5. Validate `--threads` so `0` and negative values are rejected cleanly.

## Recommended implementation order

1. Add a `tests/` directory with unit tests around:
   - sequence matching
   - missing-frame detection
   - magic-byte validation
   - current exit-code behavior
2. Split pure logic from CLI printing and exit handling.
3. Revisit operator-facing semantics only after tests cover the current contract.

## Secondary improvements

- Add explicit output when the tool is running in magic-only mode because `OpenEXR` is unavailable.
- Add `--no-color` for CI and log capture.
- Add a structured output mode such as JSON for automation.
- Add fixture-based tests for truncated files, invalid headers, empty channels, and invalid data windows.
- Consider a library entrypoint if other tools need to embed validation logic.

## Current maintenance gaps

- no test suite
- no CI
- no lint/format/typecheck configuration
- all logic concentrated in one file
- behavior depends on the local availability of the `OpenEXR` binding

## Status notes

These tasks are based on the repo as of 2026-04-01:
- branch `main`
- clean worktree
- runnable local `uv` environment present
