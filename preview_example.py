"""
Simple example showing how to preview generated opcode documentation.
Just run this script and it will show the documentation with grip.
"""

import tempfile
import subprocess
from pathlib import Path

from pmp_manip.opcode_info.doc_api.main import generate_opcode_doc
from pmp_manip import info_api


def preview_markdown_with_grip(markdown_content: str, filename: str = "opcode_preview.md"):
    """
    Preview markdown content using grip.
    
    Args:
        markdown_content: The markdown string to preview
        filename: Name for the temporary markdown file
    """
    # Write markdown to temporary file
    temp_file = Path(tempfile.gettempdir()) / filename
    temp_file.write_text(markdown_content, encoding='utf-8')
    
    print(f"Starting grip server for: {temp_file}")
    print("Press Ctrl+C to stop the server")
    
    # Run grip on the file
    subprocess.run(["grip", str(temp_file)], check=True)


def main():
    """Example usage"""
    # Example opcodes to test
    test_opcodes = [
        "&sensing::mouse x", 
        "&control::if <CONDITION> then {THEN} else {ELSE}",
    ]
    
    print("Preview opcode documentation with grip:")
    print("Make sure you have grip installed: pip install grip")
    print()
    
    # Generate and preview first opcode
    opcode = test_opcodes[0]
    doc_string = generate_opcode_doc(info_api, opcode)
    preview_markdown_with_grip(doc_string, f"opcode_{opcode.split('::')[1]}.md")


if __name__ == "__main__":
    main()
