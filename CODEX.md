# CODEX.md

## Project summary

`exr-checker` is a compact Python CLI for scanning an OpenEXR sequence and reporting corrupt frames. The implementation surface is deliberately small: almost all product behavior lives in `src/exr_checker/cli.py`.

## Files that matter first

Read these before editing:
- `src/exr_checker/cli.py`
- `README.md`
- `pyproject.toml`

That is effectively the whole product.

## Current implementation notes

`src/exr_checker/cli.py` contains:
- sequence discovery via `find_sequence_files`
- gap detection via `detect_missing_frames`
- EXR magic validation via `check_frame_magic`
- full OpenEXR validation via `check_frame_openexr`
- dispatcher logic via `check_frame`
- threaded execution and summary printing via `run`
- `argparse` setup and `sys.exit` paths via `main`

Notable details:
- `numpy` is imported only because the OpenEXR workflow depends on array-backed channel data; the code does not otherwise use the `np` name
- ANSI color sequences and block characters are emitted directly
- the progress bar is updated during `as_completed`, then results are reprinted in frame order
- the script exits from inside `run`, which makes behavior harder to test

## Current behavior contract

Input contract:
- positional argument is a full sequence prefix with a trailing dot
- `--ext` defaults to `exr`
- `--threads` defaults to `4`
- `--verbose` prints one line for each valid frame

Behavior contract:
- missing frames are informational only
- corrupt frames produce exit `2`
- runtime/argument failures produce exit `1`
- no matches produce warning + exit `0`
- OpenEXR import failure downgrades validation depth instead of aborting

## Tooling and execution

Environment:
- Python `>=3.11`
- package manager / runner: `uv`
- build backend: `hatchling`

Dependencies:
- `openexr>=3.3.0`
- `numpy>=1.24.0`

Verified locally on 2026-04-01:
- `uv run exr-check -h` works from this checkout

## Editing guidance

If you change:
- command name: update `[project.scripts]` and CLI help/examples in `cli.py` and `README.md`
- validation semantics: update `README.md` and `DECISIONS.md`
- exit codes: update `README.md`, `AGENTS.md`, and `DECISIONS.md`

Prefer these next refactors if you need to grow the project:
- move pure sequence/validation logic into testable helpers
- return structured results from `run` instead of exiting inside helper code
- add tests before changing operator-facing semantics

## Risks and gaps

Current gaps:
- no automated tests
- no fixture EXRs
- no machine-readable output mode
- no explicit validation that `--threads` is positive
- no `--no-color` mode for CI/non-TTY logs

Current semantic sharp edges:
- success exit on no matches may be surprising in automation
- success exit on missing frames may be surprising in automation
- behavior changes depending on whether `OpenEXR` imports successfully
