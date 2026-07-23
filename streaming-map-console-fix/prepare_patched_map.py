#!/usr/bin/env python3
"""Download stock map.gzd and remove the missing crossboard_res reference."""

from pathlib import Path
import urllib.request

OUT = Path(__file__).resolve().parent / "map.gzd"
URL = "https://gizmosdk.blob.core.windows.net/maps/stock/map.gzd"
NEEDLE = b"res:crossboard_res - FULL.gzd"


def main():
    print("Downloading", URL)
    data = bytearray(urllib.request.urlopen(URL, timeout=120).read())
    idx = data.find(NEEDLE)
    if idx < 0:
        print("Reference not found; writing map unchanged")
    else:
        data[idx : idx + len(NEEDLE)] = b"\0" * len(NEEDLE)
        print(f"Cleared crossboard resource URL at offset {idx}")
    OUT.write_bytes(data)
    print("Wrote", OUT, "size", OUT.stat().st_size)


if __name__ == "__main__":
    main()
