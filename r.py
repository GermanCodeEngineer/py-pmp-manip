from pmp_manip import info_api
from pmp_manip.utility import read_file_text, write_file_text
from json import dumps, loads
cats = {
    'motion': 'motion', 
    'looks': 'looks', 
    'sound': 'sound', 
    'event': 'events',
    'control': 'control', 
    'sensing': 'sensing', 
    'operator': 'operators', 
    'data': 'variables', 
    'procedures': 'customblocks', 
    'argument': 'customblocks', 
    'checkbox': 'special', 
    'polygon': 'special', 
    'note': 'special',
}

replacements = {}
for old_opcode, new_opcode in info_api.opcode_info.keys_key1_key2():
    if "::" in new_opcode: continue
    cat = old_opcode.split("_", maxsplit=1)[0]
    replacements[new_opcode] = f"{cats[cat]}::{new_opcode}"

import os
clear = lambda: os.system('clear')
    
write_file_text("r.json", dumps(replacements))

try:
    passed, questioned = loads(read_file_text("state.json"))
except:
    passed = {}
    questioned = {}
for old, new in replacements.items():
    if old in passed: continue
    if old in questioned: continue
    clear()
    print(repr(new))
    try:
        ans = input(">>> ")
    except KeyboardInterrupt:
        ans = input(">>> ")
    if ans == "!q":
        break
    elif ans:
        questioned[old] = (new, ans)
    else:
        passed[old] = new

write_file_text("state.json", dumps((passed, questioned)))
