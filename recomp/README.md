# recomp/

Analysis input for Final Fantasy V. `tools/regen.sh` reads this directory and
writes `src/gen/`.

| File | Owner | Notes |
|---|---|---|
| `bank*.cfg` | you, plus generated blocks | Per-bank analysis directives |
| `symbols.toml` | you | Progressive name map; the source of truth |
| `funcs.h` | generated | Re-synced by `tools/regen.sh` — do not hand-edit |

The block between `>>> BEGIN symbols.toml` and `<<< END symbols.toml` in
each bank cfg is rewritten from `symbols.toml` on every regen. Missing bank
configs are created automatically; hand-written directives outside the blocks
are preserved. Removing a symbol removes its generated directives on the next
regen. Do not edit the generated blocks.

This synchronization is provided by the pinned snesrecomp framework through
`snesrecomp_cli.py generate`. After updating this repository, run
`git submodule update --init --recursive` to use its framework pin.
Python 3.11+ includes the TOML reader; on older Python, install the backport
with `python -m pip install tomli`.

- `emit = false` creates a friendly `symbol` label and a `force_lle` boundary,
  keeping that entry interpreted. It does not add a compiled `func` or a
  declaration in `funcs.h`.
- `emit = true` creates a `func` and requests ahead-of-time analysis, even
  without `--cfg-roots`. Only variants the analyzer proves safe become compiled
  code. Optional `entry_m` and `entry_x` set the entry register-width flags
  (0 or 1, both default to 1).

The imported map currently sets every entry to `emit = false`. Synchronizing
it therefore imports labels and interpreter choices, rather than compiling
every listed function. `src/gen/bank*_v2.c` can also be generated from code
discovered through ROM control flow; those output files do not imply that every
discovered function has been written back into a cfg.

There is a tool that updates `symbols.toml` with all functions (WIP). Assuming you've opened the terminal at root folder, run:
```
python tools/rewrite_symbols.py
```

The importer rewrites the entire file and sets `emit = false` on every entry.
It can leave `addr = "XXXX"` placeholders, which must be resolved before regen.
Review its addresses and banks before promoting selected functions with
`emit = true` in `symbols.toml`. Preserve any manual edits before rerunning the
importer; it does not merge them.

No manual `bankc0.cfg` is needed merely to import bank C0 symbols. Add cfg
directives outside the generated blocks when a bank needs extra analysis hints.
