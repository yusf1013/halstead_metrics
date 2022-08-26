def get_function_lines(node, file):
    lines = file.split("\n")
    start_line = node.lineno - 1
    if hasattr(node, 'args'):
        start_line = node.args.args[0].lineno - 1
    lines = lines[start_line: node.end_lineno]
    return "\n".join(lines)


def get_stmt_types(function, file):
    types = set()
    for node in function.body:
        types.add(get_node_class(node))
        # if node.__class__.__name__ == "Expr" and node.value.__class__.__name__ == "Call":
        #     print("Expr: " + str(node.value.__class__.__name__))
        #     print(get_function_lines(node, file))

    return types


def get_node_class(node):
    return node.__class__.__name__
