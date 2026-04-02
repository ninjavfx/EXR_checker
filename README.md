# exr-checker

CLI tool for scanning an OpenEXR image sequence and reporting corrupt frames.

It checks:
- EXR magic bytes
- header parsing through the OpenEXR file API
- data window sanity
- channel readability for every frame
- gaps in the frame range

## Requirements

- Python 3.11+
- [`uv`](https://docs.astral.sh/uv/)

Project dependencies are managed through `uv`:
- `openexr>=3.3.0`
- `numpy>=1.24.0`

## Install

Clone the repo and install the environment:

```bash
git clone <repo-url> exr-checker
cd exr-checker
uv sync
```

This creates `.venv/` and installs the console scripts:
- `exr-checker`
- `check-exr`

## Usage

The tool expects a full sequence prefix including the trailing dot:

```bash
uv run exr-checker /mnt/vfx/plate/FRM_4520_plate_WTA_v000.
```

Examples:

```bash
uv run exr-checker /mnt/vfx/plate/FRM_4520_plate_WTA_v000.
uv run exr-checker /mnt/vfx/plate/FRM_4520_plate_WTA_v000. --threads 16 --verbose
uv run exr-checker /mnt/vfx/plate/FRM_4520_plate_WTA_v000. --ext exr --threads 8
uv run check-exr /mnt/vfx/plate/FRM_4520_plate_WTA_v000.
```

If you activate the virtual environment, you can run the command directly:

```bash
source .venv/bin/activate
exr-checker /mnt/vfx/plate/FRM_4520_plate_WTA_v000.
```

## CLI options

```text
usage: exr-checker [-h] [--ext EXT] [--threads THREADS] [--verbose] sequence
```

- `sequence`: full path including basename and trailing dot
- `--ext`: file extension without the dot, default `exr`
- `--threads`: worker thread count, default `4`
- `--verbose`: print a line for every valid frame

## Sequence matching

Given:

```text
/mnt/vfx/plate/FRM_4520_plate_WTA_v000.
```

the tool matches files shaped like:

```text
FRM_4520_plate_WTA_v000.1001.exr
FRM_4520_plate_WTA_v000.1002.exr
FRM_4520_plate_WTA_v000.1003.exr
```

It scans the detected frame range, reports missing frame numbers, and validates each file found on disk.

## Output behavior

The checker prints:
- sequence pattern
- worker count
- validation backend
- detected frame range
- missing frames, if any
- per-frame failures
- a final summary

Missing frames are reported in the summary, but they do not currently cause a non-zero exit by themselves. A non-zero success/failure result is driven by corrupt frames or argument/runtime errors.

## Exit codes

| Code | Meaning |
|------|---------|
| `0` | No corrupt frames found |
| `1` | CLI or runtime error |
| `2` | One or more corrupt frames found |

## Project structure

```text
exr-checker/
├── pyproject.toml
├── README.md
└── src/
    └── exr_checker/
        ├── __init__.py
        └── cli.py
```
