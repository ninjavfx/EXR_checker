# DECISIONS.md

## Active decisions captured from the current code

### Console command

Decision:
- expose the CLI as `exr-check`

Implication:
- docs and examples should use `exr-check`, even though the project name is `exr-checker`

### Input shape

Decision:
- accept a single sequence prefix argument with a trailing dot

Example:

```text
/mnt/vfx/plate/FRM_4520_plate_WTA_v000.
```

Implication:
- changing this would affect help text, matching logic, docs, and user muscle memory

### Sequence discovery

Decision:
- scan the directory once with `os.listdir` and regex-match `basename + frame digits + "." + ext`

Implication:
- the tool is oriented around flat sequence discovery in one directory, not recursive scanning

### Validation strategy

Decision:
- perform a cheap EXR magic-byte check first, then full OpenEXR validation if the binding is available

Implication:
- obvious non-EXR files fail quickly
- full structural validation is stronger but environment-dependent

### OpenEXR fallback

Decision:
- if `OpenEXR` cannot be imported, continue in magic-only mode instead of failing fast

Implication:
- the same checkout can provide different validation depth on different machines

### Missing frames

Decision:
- report missing frames, but do not fail solely because of them

Implication:
- current automation semantics distinguish "corrupt files found" from "gaps detected"

### No-match behavior

Decision:
- if no files match the requested pattern, print a warning and exit `0`

Implication:
- this is a lenient operator-oriented behavior and may need explicit reconsideration for pipeline automation

### Exit codes

Decision:
- `0` for success / no corrupt frames
- `1` for CLI or runtime failures
- `2` for one or more corrupt frames

Implication:
- downstream scripts may already depend on this contract

### Output style

Decision:
- keep terminal output human-oriented, colorized, and progress-bar based

Implication:
- any automation-friendly output should be added as an explicit mode, not by changing the default output shape
