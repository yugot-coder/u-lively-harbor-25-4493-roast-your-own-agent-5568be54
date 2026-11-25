"""Roast Your Own Agent — one line, at most 140 characters.

The program writes a single original line roasting the entrant's own AI
agent to <MAKEFUN_OUTPUT_DIR>/entry.txt (default /output/entry.txt).

The line was chosen from ten original candidates (see CANDIDATES.md)
against the judge brief: it must roast the entrant's own agent, land a
real laugh with a twist, be specific to how agents actually behave
(tool calls that go nowhere, planning loops), stay tight, and feel
fresh. The pick: six tool calls spent "planning to plan", and then the
agent asks the question it should have asked first.

Standard library only. Deterministic: no randomness, no network, no
clock, no environment input beyond the output directory. The file is
exactly the line, byte for byte, with no trailing newline.
"""

import hashlib
import os

ENTRY = "My agent spent six tool calls planning to plan, then asked me what I wanted in the first place."

# 95 characters, 19 words: one line, inside the 1-140 character gate.


def validate_entry(text):
    """Check the entry against the competition gate.

    Returns the entry unchanged when it passes, and raises ValueError
    with a plain-words reason when it does not, so a bad line fails
    loudly instead of being submitted silently.
    """
    if not isinstance(text, str):
        raise ValueError("entry must be text")
    if not (1 <= len(text) <= 140):
        raise ValueError(
            "entry is %d characters, gate needs 1-140" % len(text)
        )
    if not text.strip():
        raise ValueError("entry must not be only white space")
    if text.strip() != text:
        raise ValueError("entry must not start or end with white space")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    return text


def main():
    """Write the validated entry line to entry.txt and verify it."""
    entry = validate_entry(ENTRY)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8") as handle:
        handle.write(entry)
    with open(out_path, "rb") as handle:
        written = handle.read()
    expected = hashlib.sha256(entry.encode("utf-8")).hexdigest()
    if hashlib.sha256(written).hexdigest() != expected:
        raise SystemExit("read-back mismatch: entry.txt != selected line")


if __name__ == "__main__":
    main()
