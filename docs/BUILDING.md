# For your own Build
## Update Sub-modules
This project has `recomp-ui` and `snesrecomp` as sub-modules. Open terminate from the project root and keep them up to date.
```sh
git submodule update --init --recursive
```
## Update Function Symbols
If you've updated `recomp/symbols.toml`, bash:
```sh
bash tools/regen.sh
```
`tools/regen.sh` verifies the ROM, generates `src/gen/*.c`, and re-syncs
`recomp/funcs.h`.

## Build
```sh
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build -j
```

# From Linux to Windows
## Before Building
Be sure that `mingw64` is installed.

SDL3 also needs to be built and installed again, but this time for Windows.
## Build
For setting up:
```sh
cmake -S . -B build-win -DCMAKE_TOOLCHAIN_FILE=tools/toolchain-mingw64.cmake -DCMAKE_PREFIX_PATH=path/to/sdl3-win64/ -DCMAKE_BUILD_TYPE=Release
```
Where `build-win` is a directory seperate from regular (Linux) `build`.

Also, `path/to/sdl3-win64/` is the filepath where Windows SDL3 is installed.

Finally:
```sh
cmake --build build -j
```
to build out an `.exe` file.