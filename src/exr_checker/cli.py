#!/usr/bin/env python3
"""
EXR Sequence Corruption Checker
Uses the OpenEXR 3.3+ File API (numpy-based). No Imath import needed.
"""

import os
import sys
import re
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    import OpenEXR
    import numpy as np
    HAS_OPENEXR = True
except ImportError:
    HAS_OPENEXR = False

GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
CYAN   = "\033[96m"
RESET  = "\033[0m"
BOLD   = "\033[1m"

EXR_MAGIC = b'\x76\x2f\x31\x01'


# ── Detection ─────────────────────────────────────────────────────────────────

def find_sequence_files(directory: str, basename: str, ext: str) -> list[tuple[int, str]]:
    pattern = re.compile(
        r'^' + re.escape(basename) + r'(\d+)\.' + re.escape(ext) + r'$'
    )
    matches = []
    try:
        entries = os.listdir(directory)
    except FileNotFoundError:
        print(f"{RED}[ERROR] Directory not found: {directory}{RESET}")
        sys.exit(1)

    for entry in entries:
        m = pattern.match(entry)
        if m:
            frame = int(m.group(1))
            matches.append((frame, os.path.join(directory, entry)))

    matches.sort(key=lambda x: x[0])
    return matches


def detect_missing_frames(frame_numbers: list[int]) -> list[int]:
    if not frame_numbers:
        return []
    full = set(range(frame_numbers[0], frame_numbers[-1] + 1))
    return sorted(full - set(frame_numbers))


# ── Validation ────────────────────────────────────────────────────────────────

def check_frame_magic(filepath: str) -> tuple[bool, str]:
    """Fast check: verify EXR magic bytes."""
    try:
        with open(filepath, 'rb') as f:
            magic = f.read(4)
        if magic != EXR_MAGIC:
            return False, f"Invalid magic bytes: {magic.hex()}"
        return True, "ok"
    except OSError as e:
        return False, str(e)


def check_frame_openexr(filepath: str) -> tuple[bool, str]:
    """
    Full validation using the OpenEXR 3.3+ File API:
      1. File opens and header parses without error.
      2. Data window is sane (positive dimensions).
      3. Every channel can be read into a numpy array and is non-empty.
    """
    try:
        with OpenEXR.File(filepath, separate_channels=True) as exr:
            header = exr.header()

            dw = header.get("dataWindow")
            if dw is not None:
                dw_min, dw_max = dw
                width  = int(dw_max[0]) - int(dw_min[0]) + 1
                height = int(dw_max[1]) - int(dw_min[1]) + 1
                if width <= 0 or height <= 0:
                    return False, f"Invalid data window: {width}x{height}"

            channels = exr.channels()
            if not channels:
                return False, "No channels found in header"

            for ch_name, ch in channels.items():
                pixels = ch.pixels
                if pixels is None or pixels.size == 0:
                    return False, f"Channel '{ch_name}' returned empty array"

    except Exception as e:
        return False, str(e)

    return True, "ok"


def check_frame(filepath: str) -> tuple[bool, str]:
    """Dispatch: magic check first, then full OpenEXR validation if available."""
    ok, reason = check_frame_magic(filepath)
    if not ok:
        return False, reason
    if HAS_OPENEXR:
        return check_frame_openexr(filepath)
    return True, "ok (magic-only)"


# ── Runner ────────────────────────────────────────────────────────────────────

def run(directory: str, basename: str, ext: str, threads: int, verbose: bool):
    print(f"\n{BOLD}{CYAN}EXR Sequence Checker{RESET}")
    print(f"  Sequence  : {os.path.join(directory, basename)}<FRAME>.{ext}")
    print(f"  Threads   : {threads}")
    print(f"  Backend   : {'OpenEXR 3.3+ full validation' if HAS_OPENEXR else 'magic-bytes only'}\n")

    files = find_sequence_files(directory, basename, ext)

    if not files:
        print(f"{YELLOW}[WARN] No files found matching {basename}<FRAME>.{ext}{RESET}")
        sys.exit(0)

    frame_numbers = [f for f, _ in files]
    missing = detect_missing_frames(frame_numbers)

    print(f"  Found  : {len(files)} frame(s)  [{frame_numbers[0]} - {frame_numbers[-1]}]")
    if missing:
        print(f"  {YELLOW}Missing: {len(missing)} frame(s) -> "
              f"{missing[:10]}{'...' if len(missing) > 10 else ''}{RESET}")
    else:
        print(f"  {GREEN}No missing frames detected{RESET}")
    print()

    corrupt: list[tuple[int, str, str]] = []
    good = 0
    results: dict[int, tuple[bool, str]] = {}

    with ThreadPoolExecutor(max_workers=threads) as pool:
        future_map = {pool.submit(check_frame, path): (frame, path) for frame, path in files}
        done = 0
        total = len(files)
        for future in as_completed(future_map):
            frame, path = future_map[future]
            ok, reason = future.result()
            results[frame] = (ok, reason)
            done += 1
            bar = int((done / total) * 40)
            print(f"\r  [{GREEN}{'█' * bar}{RESET}{'░' * (40 - bar)}] {done}/{total}",
                  end='', flush=True)

    print()
    print()

    for frame, path in files:
        ok, reason = results[frame]
        fname = os.path.basename(path)
        if ok:
            good += 1
            if verbose:
                print(f"  {GREEN}✔{RESET}  {fname}")
        else:
            corrupt.append((frame, fname, reason))
            print(f"  {RED}✘  {fname}{RESET}")
            print(f"      └─ {reason}")

    print()
    print(f"{BOLD}─── Summary ───────────────────────────────────────{RESET}")
    print(f"  Total frames  : {total}")
    print(f"  {GREEN}Good          : {good}{RESET}")
    if missing:
        print(f"  {YELLOW}Missing       : {len(missing)}{RESET}")
    if corrupt:
        print(f"  {RED}Corrupt       : {len(corrupt)}{RESET}")
        print(f"\n  {BOLD}Corrupted frames:{RESET}")
        for frame, fname, reason in corrupt:
            print(f"    Frame {frame:>6}  {fname}")
            print(f"      └─ {reason}")
        print()
        sys.exit(2)
    else:
        print(f"\n  {GREEN}{BOLD}All frames OK.{RESET}\n")
        sys.exit(0)


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Check an EXR image sequence for corrupted or missing frames.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  exr-checker /mnt/vfx/plate/FRM_4520_plate_WTA_v000.
  exr-checker /mnt/vfx/plate/FRM_4520_plate_WTA_v000. --threads 16 --verbose
  exr-checker /mnt/vfx/plate/FRM_4520_plate_WTA_v000. --ext exr --threads 8
        """
    )
    parser.add_argument(
        "sequence",
        help="Full path including basename and trailing dot, "
             "e.g. /mnt/plate/FRM_4520_plate_WTA_v000."
    )
    parser.add_argument("--ext",     default="exr", help="File extension without dot (default: exr)")
    parser.add_argument("--threads", type=int, default=4, help="Parallel worker threads (default: 4)")
    parser.add_argument("--verbose", action="store_true", help="Print a line for every frame")

    args = parser.parse_args()

    # Split /path/to/dir/basename. -> directory=/path/to/dir  basename=basename.
    sequence  = os.path.abspath(args.sequence)
    directory = os.path.dirname(sequence)
    basename  = os.path.basename(sequence)

    if not basename:
        parser.error("Could not determine basename from the given path.")

    run(
        directory=directory,
        basename=basename,
        ext=args.ext.lstrip('.'),
        threads=args.threads,
        verbose=args.verbose,
    )


if __name__ == "__main__":
    main()
