# TASKS.md

## High-value next tasks

1. Add automated tests for sequence matching, missing-frame detection, exit codes, and corruption reporting.
2. Separate pure validation logic from CLI printing so behavior can be tested without invoking `sys.exit`.
3. Decide whether missing frames should produce a non-zero exit code; current behavior only reports them.
4. Decide whether "no files found" should remain exit `0` or become a failure/warning code for pipeline usage.
5. Add input validation for invalid `--threads` values such as `0` or negative numbers.
6. Consider a `--no-color` flag for CI logs and non-TTY environments.
7. Consider explicit fallback messaging when `OpenEXR` is unavailable and only magic-byte checks are performed.
8. Add fixture-based tests for broken headers, empty channels, invalid data windows, and truncated files.
9. Consider structured output mode such as JSON for pipeline automation.
10. Keep README examples and alias guidance aligned with the active console script name `exr-check`.

## Current maintenance gaps

- No test suite
- No linting or formatting config
- No CI configuration
- CLI and business logic are tightly coupled in one file
- Runtime behavior depends on the presence of the OpenEXR Python binding

## Suggested order

1. Add tests around current behavior before changing semantics.
2. Refactor `cli.py` into more testable units without changing output.
3. Revisit missing-frame and no-files exit semantics once tests lock down expectations.
