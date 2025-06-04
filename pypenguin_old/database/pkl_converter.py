import os
import pickle
import importlib.util
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from pypenguin_old.utility import ensureCorrectPath
FOLDER_PATH = ensureCorrectPath("src/pypenguin/database/beautiful/", "PyPenguin")
OUTPUT_FILE = ensureCorrectPath("src/pypenguin/database/database.pkl", "PyPenguin")

combined_opcodes = {}

# Loop through all .py files in the folder
print(os.listdir(FOLDER_PATH))
for filename in os.listdir(FOLDER_PATH):
    if filename.endswith(".py") and filename != "__init__.py":
        file_path = os.path.join(FOLDER_PATH, filename)

        # Load the module dynamically
        module_name = filename[:-3]  # Remove ".py"
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Extract opcodes if it exists in the module
        if hasattr(module, "opcodes") and isinstance(module.opcodes, dict):
            combined_opcodes.update(module.opcodes)  # Merge dictionaries

print(f"✅ Merged {len(combined_opcodes)} opcodes from {FOLDER_PATH}")

# Save as Pickle (fastest format for Python)
with open(OUTPUT_FILE, "wb") as f:
    pickle.dump(combined_opcodes, f, protocol=pickle.HIGHEST_PROTOCOL)

print(f"✅ Saved combined opcodes to {OUTPUT_FILE}")
