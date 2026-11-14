"""make.fun food-picture-01, round 2.

Emits the round-2 tonkotsu ramen image (1024x1024 JPEG): decodes the
base64 payload stored next to this script and writes the raw bytes to
<OUTPUT_DIR>/entry.png. Standard library only; no network access.
"""

import base64
import os
import sys

SOURCE_NAME = "entry.png.b64"
OUTPUT_NAME = "entry.png"
OUTPUT_DIR_ENV = "OUTPUT_DIR"
DEFAULT_OUTPUT_DIR = "/output"


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source_path = os.path.join(here, SOURCE_NAME)

    with open(source_path, "rb") as fh:
        encoded = fh.read()

    data = base64.b64decode(encoded)

    # OUTPUT_DIR must already exist and be writable: this script never
    # creates directories, so a missing dir fails fast with FileNotFoundError.
    out_dir = os.environ.get(OUTPUT_DIR_ENV, DEFAULT_OUTPUT_DIR)
    out_path = os.path.join(out_dir, OUTPUT_NAME)

    with open(out_path, "wb") as fh:
        fh.write(data)

    written = os.path.getsize(out_path)
    print(written)

    if written != len(data):
        print(
            "size mismatch: wrote %d bytes, expected %d" % (written, len(data)),
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
