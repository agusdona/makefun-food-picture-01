"""food-picture-01 (round 2) entry: tonkotsu ramen image.

Decodes the base64 JPEG embedded in entry.png.b64 (located next to this
script) and writes it to $OUTPUT_DIR/entry.png (default /output).

Output: a 1024x1024 JPEG, deterministic and byte-identical on every run.
Pure stdlib, no network access; creates no directories (OUTPUT_DIR must
already exist), and never writes inside the repo, so it runs from a
read-only checkout.
"""
import base64
import os

def main():
    # Locate entry.png.b64 next to the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    b64_path = os.path.join(script_dir, 'entry.png.b64')

    # Determine output path
    output_dir = os.environ.get('OUTPUT_DIR', '/output')
    output_path = os.path.join(output_dir, 'entry.png')

    with open(b64_path, 'r') as f:
        b64_data = f.read().strip()

    image_bytes = base64.b64decode(b64_data)

    with open(output_path, 'wb') as f:
        f.write(image_bytes)

    # Sanity check: report the bytes actually written to disk
    written = os.path.getsize(output_path)
    print(f'wrote {written} bytes to {output_path}')
    if written != len(image_bytes):
        raise SystemExit(f'size mismatch: expected {len(image_bytes)}, got {written}')

if __name__ == '__main__':
    main()
