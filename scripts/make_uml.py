from dataclasses import is_dataclass, fields
from typing import get_origin, get_args, get_type_hints
from types import UnionType, NoneType
import inspect
import sys
from graphviz import Digraph


SKIP_TYPES = {int, str, float, bool, bytes, bytearray, complex, type(None)}

def _repr_t(t: type) -> str:
    origin = get_origin(t)
    args = get_args(t)

    if origin is UnionType:
        tname = " | ".join(_repr_t(subt) for subt in args)
    elif origin in (list, tuple, set):
        inner = ", ".join(_repr_t(subt) for subt in args)
        tname = f"{origin.__name__}[{inner}]"
    elif t is NoneType:
        tname = str(None)
    elif hasattr(t, "__name__"):
        tname = getattr(t, "__name__")
    return tname


def escape_label(text: str) -> str:
    """Escape Graphviz special chars like | and {}."""
    return text.replace("|", "\\|").replace("{", "\\{").replace("}", "\\}")

def resolve_type(tp):
    """Extract the base type from generic/union annotations."""
    origin = get_origin(tp)
    if origin is None:
        return tp
    if origin in (list, tuple, set):
        return resolve_type(get_args(tp)[0])
    if origin is dict:
        return resolve_type(get_args(tp)[1])
    if origin is type(None):
        return None
    args = [a for a in get_args(tp) if a is not type(None)]
    if args:
        return resolve_type(args[0])
    return tp

def walk_related_classes(root_cls, seen=None):
    """Collect all dataclasses reachable via inheritance or composition."""
    if seen is None:
        seen = set()
    if root_cls in seen:
        return seen
    seen.add(root_cls)

    # Inheritance
    for sub in root_cls.__subclasses__():
        walk_related_classes(sub, seen)

    # Composition
    if is_dataclass(root_cls):
        hints = get_type_hints(root_cls, globalns=sys.modules[root_cls.__module__].__dict__)
        for _, field_type in hints.items():
            base = resolve_type(field_type)
            if inspect.isclass(base) and is_dataclass(base) and base not in SKIP_TYPES:
                walk_related_classes(base, seen)
    return seen

def format_class_label(cls):
    """Create UML-like label for a dataclass."""
    attrs = []
    if is_dataclass(cls):
        hints = get_type_hints(cls, globalns=sys.modules[cls.__module__].__dict__)
        for fname, ftype in hints.items():
            tname = _repr_t(ftype)
            tname = escape_label(tname)
            attrs.append(f"{fname}: {tname}")
    else:
        attrs.append("<< not a dataclass >>")
    attr_str = "\\l".join(attrs) + "\\l" if attrs else ""
    return f"{{{escape_label(cls.__name__)}|{attr_str}}}"

def build_diagram(root_cls, filename="uml_tree"):
    dot = Digraph(comment="Dataclass UML", format="svg")
    dot.attr(rankdir="LR", dpi="300")  # Left-to-right layout, high resolution
    dot.attr("node", shape="record", fontname="Helvetica", fontsize="10",
             style="filled", fillcolor="#f9f9f9", color="#555555")
    dot.attr("edge", fontname="Helvetica", fontsize="9", color="#333333")

    classes = walk_related_classes(root_cls)

    # Add nodes
    for cls in classes:
        dot.node(cls.__name__, format_class_label(cls))

    # Add edges
    for cls in classes:
        for sub in cls.__subclasses__():
            if sub in classes:
                dot.edge(cls.__name__, sub.__name__, arrowhead="onormal", color="#0066cc", penwidth="1.2")
        if is_dataclass(cls):
            hints = get_type_hints(cls, globalns=sys.modules[cls.__module__].__dict__)
            for _, ftype in hints.items():
                fbase = resolve_type(ftype)
                if inspect.isclass(fbase) and is_dataclass(fbase) and fbase in classes:
                    dot.edge(cls.__name__, fbase.__name__, arrowhead="diamond", color="#ff6600", penwidth="1.2")

    output_path = dot.render(filename, cleanup=True)
    print(f"Diagram saved as {output_path}")

if __name__ == "__main__":
    module_name, base_name = sys.argv[1], sys.argv[2]
    mod = __import__(module_name, fromlist=[base_name])
    base_cls = getattr(mod, base_name)
    build_diagram(base_cls, filename="docs/images/second_repr_uml")