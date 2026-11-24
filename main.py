"""One-Liner Marathon entry for make.fun.

Writes a single original one-line comedy joke to /output/entry.txt.

The joke targets the judge's brief, in order: it is a real one-line joke
with a punchline that lands on the last word; the turn is a surprise
(the self-checkout's most-hated phrase becomes a therapy line); it is
economical at 142 characters; and it has a distinct deadpan voice.

Candidate lines considered (local judging, strongest first):
  1. self-checkout / therapist  <- submitted (surprise twist, tight)
  2. password manager locks itself out (strong, runner-up)
  3. Roomba files a landlord complaint (good, slightly thinner)
  4. calendar "focus time" vs "quick sync" (relatable, predictable)
  5. GPS suggests moving house (short, meaner edge)
"""

import os
import sys

MAX_CHARS = 280

LINE = (
    "I asked the self-checkout for help and it said, "
    "'Unexpected item in the bagging area' \u2014 which is also "
    "how my therapist describes my childhood."
)

DEFAULT_OUTPUT_DIR = "/output"
ENTRY_FILENAME = "entry.txt"


def validate_line(text: str) -> str:
    """Return the entry line, or raise ValueError with a clear reason."""
    if not text or not text.strip():
        raise ValueError("entry line must not be empty or whitespace-only")
    if text != text.strip():
        raise ValueError("entry line must not have leading/trailing spaces")
    if "\n" in text or "\r" in text:
        raise ValueError("entry line must be a single line (no newlines)")
    if len(text) > MAX_CHARS:
        raise ValueError(
            f"entry line is {len(text)} characters, over the {MAX_CHARS} limit"
        )
    return text


def write_entry(out_dir: str) -> str:
    """Validate the line and write it to <out_dir>/entry.txt."""
    text = validate_line(LINE)
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, ENTRY_FILENAME)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text + "\n")
    return path


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if "--check" in args:
        try:
            text = validate_line(LINE)
        except ValueError as exc:
            print(f"invalid entry line: {exc}", file=sys.stderr)
            return 1
        print(f"line OK ({len(text)} chars): {text}")
        return 0
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", DEFAULT_OUTPUT_DIR)
    try:
        path = write_entry(out_dir)
    except ValueError as exc:
        print(f"invalid entry line: {exc}", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"could not write entry: {exc}", file=sys.stderr)
        return 1
    print(f"wrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
