#!/usr/bin/env python3
"""
Compress stdin using raw DEFLATE and output URL-safe base64.

This is the exact equivalent of the browser's CompressionStream("deflate-raw"):
  - zlib.compress with wbits=-15 = raw deflate (no zlib header/checksum)
  - base64 URL-safe encoding (+ → -, / → _, no padding)

Usage:
    python3 compress.py < file.md
    cat file.md | python3 compress.py
"""
import sys
import zlib
import base64

data = sys.stdin.buffer.read()
compressed = zlib.compress(data, level=9, wbits=-15)
b64 = base64.b64encode(compressed).decode()
url_safe = b64.replace("+", "-").replace("/", "_").rstrip("=")
print(url_safe, end="")