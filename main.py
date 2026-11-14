"""Molten Smash Burger bounty entry.

This program writes the bundled image bytes to the MAKEFUN_OUTPUT_DIR
(default /output) as entry.png implied by the entry.png.b64 sibling file.
It performs no network access and no filesystem writes other than that
single output file. Standard library only, no mkdir, deterministic.
"""

import base64
import os
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    b64_path = os.path.join(here, "entry.png.b64")

    with open(b64_path, "rb") as fh:
        encoded = fh.read()

    data = base64.b64decode(encoded)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    out_path = os.path.join(out_dir, "entry.png")

    with open(out_path, "wb") as fh:
        fh.write(data)

    return 0


if __name__ == "__main__":
    sys.exit(main())