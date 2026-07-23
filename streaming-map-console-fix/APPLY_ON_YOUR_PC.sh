#!/usr/bin/env bash
set -euo pipefail
# Run this inside your CSW-TEST-Streaming_Map_Demo repo root:
#   bash APPLY_ON_YOUR_PC.sh
# Or:
#   git apply streaming-map-console-fix/0001-Silence-known-Streaming-Map-Demo-console-noise.patch

ROOT="$(pwd)"
if [[ ! -f "com.saab.map-streamer/Runtime/Saab.Unity/Saab.Unity.Initializer/Initializer.cs" ]]; then
  echo "Run this from the CSW-TEST-Streaming_Map_Demo repo root."
  exit 1
fi

PATCH="$(dirname "$0")/0001-Silence-known-Streaming-Map-Demo-console-noise.patch"
if [[ ! -f "$PATCH" ]]; then
  PATCH="$ROOT/0001-Silence-known-Streaming-Map-Demo-console-noise.patch"
fi

git apply "$PATCH"
echo "Applied. Commit with:"
echo "  git add -A && git commit -m 'Silence known Streaming Map Demo console noise' && git push"
