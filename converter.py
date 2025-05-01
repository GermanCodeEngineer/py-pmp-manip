import ast
import astunparse
import re

def convert_docstring_to_google(docstring, funcdef):
    if not docstring:
        return '"""No docstring provided."""'

    indent = ' ' * 4
    if funcdef.body:
        first_stmt = funcdef.body[0]
        if hasattr(first_stmt, 'col_offset'):
            indent = ' ' * first_stmt.col_offset

    # Initialize docstring lines
    doc_lines = [f'']

    # Add the first line (summary)
    summary = docstring.strip().split("\n")[0]
    doc_lines.append(f"{indent}{summary}")
    doc_lines.append(f"{indent}")

    # Find parameters using regex for :param
    args_section = []
    param_pattern = re.compile(r':param (\S+): (.+)')
    for match in param_pattern.finditer(docstring):
        param_name = match.group(1)
        param_desc = match.group(2)
        args_section.append(f"{indent}    {param_name}: {param_desc}")

    # If there are no params in the original docstring, add placeholders
    if not args_section:
        for arg in funcdef.args.args:
            if arg.arg not in ('self', 'cls'):
                args_section.append(f"{indent}    {arg.arg}: Description")

    # If there are args, add them to the docstring
    if args_section:
        doc_lines.append(f"{indent}Args:")
        doc_lines += args_section
        doc_lines.append(f"{indent}")

    # Handle return section using regex for :return
    return_section = []
    return_pattern = re.compile(r':return: (.+)')
    return_match = return_pattern.search(docstring)
    if return_match:
        return_desc = return_match.group(1)
        return_section.append(f"{indent}    {return_desc}")

    # If there is no return section, use a default placeholder
    if return_section:
        doc_lines.append(f"{indent}Returns:")
        doc_lines += return_section

    # Close the docstring
    doc_lines.append(f'{indent}')
    doc_string = ("\n".join(doc_lines))
    return doc_string


class DocstringConverter(ast.NodeTransformer):
    def visit_FunctionDef(self, node):
        self.generic_visit(node)
        if not node.body:
            return node

        docstring = ast.get_docstring(node, clean=False)
        if docstring:
            node.body = node.body[1:]  # Remove old docstring
        new_docstring = convert_docstring_to_google(docstring, node)
        if new_docstring:
            new_doc = ast.Expr(value=ast.Constant(value=new_docstring, kind=None))
            node.body.insert(0, new_doc)
        return node


def convert_file(input_path: str, output_path: str):
    with open(input_path, 'r', encoding='utf-8') as f:
        source = f.read()

    tree = ast.parse(source)
    converter = DocstringConverter()
    tree = converter.visit(tree)
    ast.fix_missing_locations(tree)

    try:
        new_source = ast.unparse(tree)
    except AttributeError as e:
        print("Unparse error:", e)
        raise

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(new_source)

import os
def convert_folder(input_dir: str, output_dir: str):
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.py'):
                input_path = os.path.join(root, file)
                relative_path = os.path.relpath(input_path, input_dir)
                output_path = os.path.join(output_dir, relative_path)
                print(f"Converting {input_path} -> {output_path}")
                convert_file(input_path, output_path)

# Example usage:
convert_folder('pypenguin/core', 'pypenguin/core_converted')
