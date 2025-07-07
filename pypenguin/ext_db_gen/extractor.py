import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)))


from py_mini_racer import py_mini_racer
from json          import loads
from pypenguin.utility import grepr

def extract_getinfo_from_js(stub_path, js_path):
    with open(stub_path, "r", encoding="utf-8") as f:
        scratch_stub = f.read()
    with open(js_path, "r", encoding="utf-8") as f:
        extension_code = f.read()

    ctx = py_mini_racer.MiniRacer()
    
    # Concatenate and eval both files as one block of JS
    ctx.eval(scratch_stub + "\n" + extension_code)

    # Then extract the getInfo return value
    json_str = ctx.eval("JSON.stringify(_scratchExtension.getInfo());")
    info_dict = loads(json_str)
    return info_dict

# Example usage:
if __name__ == "__main__":
    stub_path = "pypenguin/ext_db_gen/scratch-stub.js"
    example_path = "pypenguin/ext_db_gen/example.js"
    
    info = extract_getinfo_from_js(stub_path, example_path)
    print(grepr(info))
