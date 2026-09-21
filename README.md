# Final Fantasy V Recomp

A native recompilation of **Final Fantasy V** (JPN), built on
[snesrecomp](https://github.com/RetroPortingToolKit/snesrecomp).

Final Fantasy V is a 1992 role-playing video game developed and published by Square for the Super Famicom. It is the fifth main installment of the Final Fantasy series.

_Description from [Wikipedia](https://en.wikipedia.org/wiki/Final_Fantasy_V), CC BY-SA 4.0._

> **You must legally own a copy of the game.** No ROM data is distributed with
> this project, in the repository or in any release. The recompiled C is
> generated locally from your own copy and is never committed.

## Status

Scaffolded on 2026-09-19 — **not yet a working port.** The layout, build,
regeneration pipeline, CI, and packaging are wired up; the game does not run
until the host work in `src/game_rtl.c` is done. See
[Porting from here](#porting-from-here).

## ROM identity

| | |
|---|---|
| File | `ffv-jp.sfc` |
| Publisher | Square |
| Developer | TOSE |
| Year | 1992 |
| Mapping | hirom |
| Region | JPN (Japan) |
| Coprocessor | none |
| CRC32 | `c1bc267d` |
| SHA-256 | `c6858d5c02894a6cc71f4dd452c7f288b319d1952ca56fdb185b4bf5e26244a2` |

`tools/regen.sh` refuses to run against anything else, so a mismatched
revision fails immediately instead of producing subtly wrong output.

## Build

```sh
git submodule update --init --recursive
bash tools/regen.sh --rom /path/to/ffv-jp.sfc
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build -j
```

The ROM does not have to live in the repository — keeping it on your own
drive is the better habit, and `SNESRECOMP_ROM` sets the path once for a
shell. `tools/regen.sh` also finds `ffv-jp.sfc` at the repo root if you
prefer that; `.gitignore` blocks it from ever being committed either way.

`tools/regen.sh` verifies the ROM, generates `src/gen/*.c`, and re-syncs
`recomp/funcs.h`. Re-run it whenever you change anything under `recomp/`.

## Run

```sh
./build/FinalFantasyVSNESRecomp                     # launcher picks the ROM
./build/FinalFantasyVSNESRecomp /path/to/ffv-jp.sfc # or name it and skip the launcher
```

With no ROM on the command line the build opens the recomp-ui launcher: a ROM
picker with a verification badge, plus display / audio / input settings. Your
choice is cached in `rom.cfg` beside the executable, so the next launch opens
on it and "Skip launcher on boot" makes it immediate. If the launcher is not
built in (`--no-recomp-ui`), the host falls back to a native file picker.

Either way the ROM is checked against the digests above before anything boots
— a dump that could not have produced this build is refused at the door rather
than mis-executing ten frames in.

## Layout

| Path | What lives there |
|---|---|
| `recomp/` | Analysis input: `bank*.cfg`, `symbols.toml`, generated `funcs.h` |
| `rom_identity.txt` | ROM digests — read by the build, `tools/regen.sh` and CI |
| `src/` | Host code you own: `main.c`, `game_rtl.c` |
| `src/gen/` | Generated C. Never committed — regenerate locally |
| `snesrecomp/` | Framework submodule (owns `lib/recomp-net`, `lib/retcomm-rbengine`) |
| `tools/` | `regen.sh` — the ROM → C pipeline |
| `scripts/` | `package_release.sh` — player-facing zip |
| `framework_pins.txt` | Exact framework commits this project was scaffolded against |

## Porting from here

The scaffold stops where the game-specific work starts. In rough order:

1. **Make it boot.** `src/game_rtl.c` holds the frame driver. The generic
   LLE-first shape is there; a real title usually needs a frame boundary and
   NMI delivery that understand its own main loop. This is the bulk of the
   work.
2. **Name things.** Add entries to `recomp/symbols.toml` as you identify
   routines, then re-run `tools/regen.sh`. Set `emit = true` to promote one
   into ahead-of-time codegen; leave it false to keep it interpreted.
3. **Resolve dispatch misses.** After every run, deal with unresolved
   indirect targets before anything else — they are the reason a port
   diverges, and they are cheap to fix early.
4. **Never synthesise a result** to get past uncovered code, and never edit
   `src/gen/` by hand. Fix the config or the framework and regenerate.

## Multiplayer

Two players, one controller per port.

## License

This project's own source is under the license in `LICENSE`. The framework
carries its own terms — see `snesrecomp/LICENSE` and
`snesrecomp/THIRD_PARTY_ATTRIBUTION.md`. Neither covers the game data, which
is not distributed here.

## Acknowledgements
* everything8215's [ff5 Disassembly](https://github.com/everything8215/ff5) is used for smybol mapping.