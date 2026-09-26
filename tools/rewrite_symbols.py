def write_func(file_sym, func_name, func_addr, func_bank):
    file_sym.write(f"""
        [[func]]
        name = \"{func_name}\"
        addr = \"{func_addr}\"
        bank = \"{func_bank}\"
        emit = false
        
    """)