# Session Snapshot

Date:
- 2026-04-01

Repository:
- path: `/home/ale/03_CODE/python/EXR_checker`
- branch: `main`
- HEAD: `0b5b0f8` (`deleted`)
- worktree: clean at time of inspection before these handoff docs were regenerated

Observed project layout:
- `README.md`
- `pyproject.toml`
- `uv.lock`
- `src/exr_checker/__init__.py`
- `src/exr_checker/cli.py`

What the project currently is:
- a small Python 3.11+ CLI for scanning EXR sequences
- uses `uv` for dependency management and execution
- exposes `exr-check` via `[project.scripts]`
- depends on `openexr>=3.3.0` and `numpy>=1.24.0`

Runtime verification performed:
- `uv run exr-check -h` succeeded on this workstation

Important current behavior:
- the positional input is a sequence prefix with a trailing dot
- matching is done in one directory using a basename-plus-frame-number pattern
- missing frames are reported but do not trigger a non-zero exit
- corrupt frames trigger exit `2`
- no matches trigger a warning and exit `0`
- if `OpenEXR` import fails, the tool still runs in magic-only mode

Recent history relevant to handoff docs:
- `HEAD` deleted the previous `CODEX.md`, `DECISIONS.md`, and `TASKS.md`
- those files were rebuilt from current source behavior rather than restored verbatim

Recommended starting point for the next Codex session:
1. Read `AGENTS.md`.
2. Read `CODEX.md`.
3. Open `src/exr_checker/cli.py`, `README.md`, and `pyproject.toml`.
4. If behavior changes are planned, add tests first.
