# recomp/

Analysis input for Final Fantasy V. `tools/regen.sh` reads this directory and
writes `src/gen/`.

| File | Owner | Notes |
|---|---|---|
| `bank00.cfg` | you, plus a generated block | Seed config for bank $00 |
| `symbols.toml` | you | Progressive name map; the source of truth |
| `funcs.h` | generated | Re-synced by `tools/regen.sh` — do not hand-edit |

The block between `>>> BEGIN symbols.toml` and `<<< END symbols.toml` in
`bank00.cfg` is rewritten from `symbols.toml` on every regen. Do not edit the block.

There is a tool that updates `symbols.toml` with all functions (WIP). Assuming you've opened the terminal at root folder, run:
```
python tools/rewrite_symbols.py
```

Editing `symbols.toml` is not recommended.

Add a bank by creating `bankNN.cfg` alongside this file; the generator picks
up every `bank*.cfg` in the directory.
