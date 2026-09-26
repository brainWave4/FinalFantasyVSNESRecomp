import pathlib
import textwrap

def write_intro(file_sym):
    file_sym.write(textwrap.dedent(f'''\
        # Progressive symbol map for Final Fantasy V.
        #
        # Each [[func]] names an address the analyzer should treat as a function.
        # Set emit = true to promote one into ahead-of-time codegen; leave it false
        # to keep it interpreted. tools/regen.sh syncs this into recomp/bank00.cfg
        # and recomp/funcs.h — do not hand-edit the generated blocks there.

        [[func]]
        name = "I_RESET"
        addr = "cec0"
        bank = 0
        emit = false
        note = "Emulation RESET vector ($FFFC)"

        [[func]]
        name = "I_NMI"
        addr = "cee0"
        bank = 0
        emit = false
        note = "Native NMI vector ($FFEA)"
    '''))

def write_func(file_sym, func_name, func_addr, func_bank):
    file_sym.write(textwrap.dedent(f'''
        [[func]]
        name = "{func_name}"
        addr = "{func_addr}"
        bank = {func_bank}
        emit = false
    '''))

FILEPATH_SYM = pathlib.Path("recomp") / "symbols.toml"

with open(FILEPATH_SYM, "w") as file_sym:
    write_intro(file_sym)

    DIR_BANKS = pathlib.Path("recomp") / "disassembly" / "src"
    ASM_EXT = ".asm"

    FILES_BANKS = {
        "field/field-main": 0xc0,
        "btlg/btlgfx-main": 0xc1,
        "battle/battle-main": 0xc2,
        "menu/menu-main": 0xc2,
        "cutscene/cutscene-main": 0xc3,
        "sound/sound-main": 0xc4
    }

    for key in FILES_BANKS:
        file_sym.write(textwrap.dedent(f'''
            # From {key}
        '''))
        
        filepath_bank = DIR_BANKS / (key + ASM_EXT)

        with open(filepath_bank) as file_bank:
            for line_bank in file_bank:
                if ":" in line_bank:
                    print(line_bank)
            
            file_bank.close()