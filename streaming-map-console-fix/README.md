# Streaming Map Demo console fix

This agent could not push directly to `CSW-TEST-Streaming_Map_Demo` (no write permission from the current Cloud Agent repo context).

## Apply on your PC

```bash
cd "~/Desktop/MyGithub Projs/CSW-TEST-Streaming_Map_Demo"
# copy the patch file into this folder, then:
git apply 0001-Silence-known-Streaming-Map-Demo-console-noise.patch
git add -A
git commit -m "Silence known Streaming Map Demo console noise"
git push origin main
```

Then reopen Unity, clear Console, and Play.

## What it fixes
- Filters missing `crossboard_res - FULL.gzd` warning
- Filters `Lock contention` / `FRAME LOST` debug spam
- Fixes `FoliagePlacement` integer modulus shader warning
