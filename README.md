# exr-checker

EXR sequence corruption checker for VFX pipelines.  
Validates every frame in a numbered sequence — checks magic bytes, header integrity,
data window sanity, and reads every channel to catch truncated writes and mid-render corruption.

---

## Requirements

- **[uv](https://docs.astral.sh/uv/)** — fast Python package/project manager
- **Python 3.11+**
- System OpenEXR libraries (needed to build the `openexr` Python binding)

---

## 1. Install uv

```bash
# macOS / Linux — one-liner installer
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or via pip if you already have Python
pip install uv
```

Restart your shell (or `source ~/.bashrc` / `source ~/.zshrc`) so `uv` is on your PATH.

---

## 2. Install system OpenEXR libraries

The `openexr` Python package is a C extension — it needs the OpenEXR dev headers/libs
on the machine before `uv sync` can build it.

### Linux — Rocky / RHEL / CentOS (typical VFX farm)

```bash
# RHEL 8 / Rocky 8 / CentOS Stream 8
sudo dnf install -y openexr-devel imath-devel gcc gcc-c++

# Older CentOS 7 (yum)
sudo yum install -y openexr-devel ilmbase-devel gcc gcc-c++
```

### macOS (artist workstations / supervisor laptops)

```bash
brew install openexr imath
```

### Ubuntu / Debian (render nodes, cloud instances)

```bash
sudo apt install -y libopenexr-dev libilmbase-dev build-essential
```

---

## 3. Clone / copy the project

```bash
# If using git
git clone <your-repo-url> exr-checker
cd exr-checker

# Or just copy the folder to the workstation and cd into it
cd exr-checker
```

---

## 4. Create the environment and install

```bash
uv sync
```

That's it. `uv` will:
- Create a `.venv` inside the project folder
- Resolve and install `openexr` and `imath` into it
- Install the `exr-checker` CLI entry point

---

## 5. Run the tool

```bash
# Activate the venv (optional — uv run works without it)
source .venv/bin/activate
exr-checker /mnt/vfx/plate FRM_4520_plate_WTA_v000.

# Or run without activating
uv run exr-checker /mnt/vfx/plate FRM_4520_plate_WTA_v000.

# With options
uv run exr-checker /mnt/vfx/plate FRM_4520_plate_WTA_v000. --threads 16 --verbose
uv run exr-checker /mnt/vfx/plate FRM_4520_plate_WTA_v000. --ext exr --threads 8
```

---

## Deploying to multiple workstations

The fastest repeatable deploy is:

```bash
# On each workstation (after system libs are installed):
git clone <repo> exr-checker && cd exr-checker && uv sync
```

Or if you can't use git, rsync the folder:

```bash
rsync -av exr-checker/ artist@workstation-42:/tools/exr-checker/
ssh artist@workstation-42 "cd /tools/exr-checker && uv sync"
```

### Optional: add to PATH system-wide

Add an alias or wrapper in `/etc/profile.d/vfx_tools.sh` so artists don't need to
cd into the project dir:

```bash
# /etc/profile.d/vfx_tools.sh
alias exr-checker="uv run --project /tools/exr-checker exr-checker"
```

---

## Project structure

```
exr-checker/
├── pyproject.toml          # project metadata, dependencies, entry point
├── README.md
└── src/
    └── exr_checker/
        ├── __init__.py
        └── cli.py          # all logic + argparse entry point
```

---

## Exit codes

| Code | Meaning                          |
|------|----------------------------------|
| `0`  | All frames OK                    |
| `2`  | One or more corrupt frames found |

This makes it safe to use in shell pipelines:

```bash
uv run exr-checker /mnt/plate FRM_4520_plate_WTA_v000. || echo "SEQUENCE HAS ERRORS"
```
