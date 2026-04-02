# CODEX.md

## Project summary

This repository is a small Python CLI for validating numbered OpenEXR sequences.
The package name is `exr-checker`, but the installed console script is currently `exr-check`.

The codebase is intentionally minimal:
- packaging in `pyproject.toml`
- implementation in `src/exr_checker/cli.py`
- no test suite
- no separate library API beyond the CLI module functions

## Current behavior

The CLI:
- accepts one positional `sequence` argument
- expects the sequence path to include the basename and a trailing dot
- defaults to `--ext exr`
- defaults to `--threads 4`
- supports `--verbose`

Matching logic:
- scans the parent directory with `os.listdir`
- matches files using `basename + frame digits + "." + ext`
- sorts by integer frame number
- detects missing frame numbers between the first and last matched frame

Validation logic:
- always checks the 4-byte EXR magic first
- if `OpenEXR` imports successfully, opens each file through `OpenEXR.File`
- validates `dataWindow` dimensions if present
- requires at least one channel
- requires each channel to return a non-empty pixel array
- falls back to magic-only validation if `OpenEXR` is unavailable

Exit behavior:
- `0` when no corrupt frames are found
- `2` when one or more corrupt frames are found
- `1` for argument/runtime failures such as missing directory
- missing frames are reported, but do not currently trigger a non-zero exit on their own
- no matched files currently returns `0` with a warning

## Environment and tooling

- Python 3.11+
- `uv` is the expected workflow for install and execution
- runtime dependencies: `openexr`, `numpy`
- build backend: `hatchling`

Useful commands:

```bash
uv sync
uv run exr-check --help
uv run exr-check /path/to/sequence_prefix.
```

## Important repo-specific notes

- There are currently uncommitted working tree changes in `README.md`, `pyproject.toml`, and `src/exr_checker/cli.py`.
- README is the main user-facing documentation and should stay aligned with the actual script name and CLI help.
- The CLI help examples are hardcoded in `src/exr_checker/cli.py`; changing command names requires updating both `pyproject.toml` and the epilog text.
- The code uses ANSI color and block characters directly in terminal output.
- `numpy` is imported only to support the OpenEXR workflow; the module does not use the `np` name directly today.
- The package/project is named `exr-checker` even though the user-facing command is `exr-check`.

## How to work safely here

- Read `pyproject.toml`, `README.md`, and `src/exr_checker/cli.py` before making changes. That is effectively the whole product surface.
- Do not assume missing frames should fail the command; that is not current behavior.
- If you change validation semantics or exit codes, update the README in the same change.
- If you add tests, prefer a small `tests/` directory with sample fixtures or mocking rather than complicating the CLI module further.
