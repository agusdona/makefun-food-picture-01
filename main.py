"""Decode entry.png.b64 and write the round-3 entry image to $OUTPUT_DIR/entry.png.

Reads entry.png.b64, which lives next to this script and holds a base64
encoding of a 1024x1024 JPEG, and writes the decoded bytes unchanged.

$OUTPUT_DIR defaults to /output. The directory must already exist (for
example as a mounted volume): this script never creates directories, and
fails with exit code 1 if the directory is missing. On success it prints
the number of bytes written and exits 0; a write error or size
mismatch also exits 1, with an error message on stderr.
"""

import base64
import binascii
import os
import sys

B64_NAME = "entry.png.b64"
OUT_NAME = "entry.png"
DEFAULT_OUTPUT_DIR = "/output"


def fail(message):
    print("error: " + message, file=sys.stderr)
    sys.exit(1)


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    b64_path = os.path.join(script_dir, B64_NAME)

    out_dir = os.environ.get("OUTPUT_DIR") or DEFAULT_OUTPUT_DIR
    if not os.path.isdir(out_dir):
        fail("output directory does not exist: " + out_dir)
    out_path = os.path.join(out_dir, OUT_NAME)

    try:
        with open(b64_path, "rb") as fh:
            encoded = fh.read()
    except OSError as exc:
        fail("cannot read " + b64_path + ": " + str(exc))

    try:
        data = base64.b64decode(b"".join(encoded.split()), validate=True)
    except (binascii.Error, ValueError) as exc:
        fail("invalid base64 in " + b64_path + ": " + str(exc))

    try:
        with open(out_path, "wb") as fh:
            written = fh.write(data)
    except OSError as exc:
        fail("cannot write " + out_path + ": " + str(exc))

    print(written)

    actual = os.path.getsize(out_path)
    if written != len(data) or actual != len(data):
        fail(
            "size mismatch: decoded %d bytes, wrote %d bytes, file is %d bytes"
            % (len(data), written, actual)
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
