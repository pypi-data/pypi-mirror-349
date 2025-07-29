'''Helper for adding source files:

Allows user to explicitly add systemverilog files that don't end in .sv using

sv@my_module.txt
v@my_verilog_module.txt
vhdl@my_vhdl_code.log

Otherwise eda.py can't know if a .txt (or .pcap, etc) file is a source file
to be part of compilation, or a file needed for simulation (.txt, .pcap, .mem
as part of a verilog $readmemh, etc)

'''

import os

# Ways to force files not ending in .sv to be systemverilog (for tools
# that require -sv vs Verilog-2001'''
FORCE_PREFIX_DICT = {
    # The values must match what's expected by eda.CommandDesign.add_file,
    # which are named in eda_config_defaults.yml - file_extensions:
    'sv@': 'systemverilog',
    'v@': 'verilog',
    'vhdl@': 'vhdl',
    'cpp@': 'cpp',
}

ALL_FORCED_PREFIXES = set(list(FORCE_PREFIX_DICT.keys()))

def get_source_file(target:str) -> (bool, str, str):
    '''Returns tuple: bool if file exists, filepath str, and optional forced file type str'''
    if os.path.exists(target):
        # target exists as a file, return True w/ original target:
        return True, target, ''

    if any(target.startswith(x) for x in ALL_FORCED_PREFIXES):
        parts = target.split('@')
        ext = parts[0]
        fpath = '@'.join(parts[1:]) # if target str had mulitple @'s
        if os.path.exists(fpath):
            # target exists as ext@fpath, return True b/c fpath exists,
            # along with the fpath and forced ext to use:
            return True, fpath, FORCE_PREFIX_DICT.get(ext + '@', '')

    # target or fpath didn't exist, return False with the original target:
    return False, target, ''
