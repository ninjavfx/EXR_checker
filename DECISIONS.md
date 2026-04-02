# DECISIONS.md

## Current decisions captured from the codebase

### Console command

Decision:
- expose a single console script named `exr-check`

Why it matters:
- user-facing docs, aliases, and CLI examples should use `exr-check`
- packaging still uses the project name `exr-checker`

### Sequence input format

Decision:
- the positional input is a sequence prefix with a trailing dot, not a directory plus basename split into separate arguments

Example:

```text
/mnt/vfx/plate/FRM_4520_plate_WTA_v000.
```

Why it matters:
- changing this would affect matching logic, help text, README examples, and user workflows

### Validation strategy

Decision:
- perform a cheap EXR magic-byte check first
- then perform full validation through `OpenEXR.File` when available

Why it matters:
- this catches obvious non-EXR files quickly
- full validation is intended to detect truncated or structurally broken files by actually reading channel data

### OpenEXR fallback

Decision:
- if importing `OpenEXR` fails, the tool still runs in magic-only mode

Why it matters:
- users may get a successful run with reduced validation depth
- documentation should not imply that full OpenEXR validation is guaranteed in every environment

### Missing frames

Decision:
- missing frame numbers are reported in output but do not currently cause a non-zero exit code

Why it matters:
- this is a meaningful product behavior choice for pipeline automation
- future changes here should be treated as a behavior change, not a refactor

### No-match behavior

Decision:
- when no files match the pattern, the tool prints a warning and exits `0`

Why it matters:
- this may be surprising in automation, but it is the current contract

### Exit codes

Decision:
- `0` for no corrupt frames
- `1` for argument/runtime failures
- `2` for one or more corrupt frames

Why it matters:
- shell usage and pipeline integration depend on these codes

### Output style

Decision:
- terminal output is human-oriented, colored, and includes a progress bar

Why it matters:
- there is currently no machine-readable output mode
- any automation-oriented output should likely be added as an explicit option rather than replacing the current format
