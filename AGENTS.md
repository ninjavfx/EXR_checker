# AGENTS.md

## Purpose

This repository is a minimal Python CLI for validating numbered OpenEXR image sequences and reporting corrupt frames.

Current package and command names:
- project/package: `exr-checker`
- console script: `exr-check`

## Repo map

Top-level files:
- `pyproject.toml`: package metadata, dependencies, console entrypoint, build backend
- `README.md`: user-facing install and usage docs
- `uv.lock`: locked dependency set for `uv`

Source:
- `src/exr_checker/__init__.py`: package marker only
- `src/exr_checker/cli.py`: all functional logic and CLI wiring

There is currently:
- no `tests/` directory
- no CI config
- no lint/format config
- no library-style public API beyond functions inside `cli.py`

## How the tool works

Expected input:
- one positional `sequence` argument
- the argument must be the full sequence prefix including the trailing dot

Example:

```text
/mnt/vfx/plate/FRM_4520_plate_WTA_v000.
```

Matching behavior:
- scan the parent directory with `os.listdir`
- match files as `basename + frame digits + "." + ext`
- parse frame numbers as integers
- sort by frame number
- detect gaps between first and last matched frame

Validation behavior:
- always verify the first 4 bytes against the EXR magic
- if `OpenEXR` imports, open via `OpenEXR.File(..., separate_channels=True)`
- validate `dataWindow` dimensions when present
- require at least one channel
- require every channel to return a non-empty pixel array
- if `OpenEXR` is unavailable, continue in magic-only mode

Exit behavior:
- `0`: no corrupt frames found
- `1`: CLI/runtime failure, such as a missing directory
- `2`: one or more corrupt frames found

Important current semantics:
- missing frames are reported but do not fail the command
- no matching files prints a warning and exits `0`

## Working conventions

When changing behavior:
- keep `README.md`, `pyproject.toml`, and `src/exr_checker/cli.py` aligned
- update CLI help examples in `cli.py` if the command shape changes
- treat exit-code changes as contract changes, not refactors

When documenting current behavior:
- do not claim missing frames fail the job; they do not today
- do not claim the tool always performs full OpenEXR validation; it can fall back to magic-only

When extending the project:
- prefer extracting pure logic from `cli.py` before adding more output branches
- add tests before changing semantics around missing frames or no-match handling

## Useful commands

```bash
uv sync
uv run exr-check -h
uv run exr-check /path/to/sequence_prefix.
```

## Current repo status snapshot

As observed on 2026-04-01:
- branch: `main`
- worktree: clean
- HEAD: `0b5b0f8` (`deleted`)
- `.venv/` exists locally but is ignored
- `uv run exr-check -h` succeeds in the checked-out environment
