from tree_sitter import Language, Parser, Node


parser = Parser()
parser.set_language(Language("build/tree_sitter_js_windows.dll", "javascript"))
code = 'console.log("Hi")'
tree = parser.parse(code)



