"""
Comment parsing
Block comment issue - Expression constant.
Reading all files.
scope handling, complex strings, new declaration for loops,  tuple declaration,
words not always separated by space
"""

import ast
import _ast
import glob

# all_file_names = glob.glob("F:\\IIT\\Projects\\PyProj" + "/**/*.py", recursive=True)
solved = ["If", "Compare", "Eq", "List", "Tuple", "IsNot", "Gt", "Lt", "NoneType", "Slice"]


def get_variables(node):
    variables = []

    if is_block_comment(node):
        return variables

    if hasattr(node, 'body'):
        if node.__class__.__name__ == "FunctionDef":
            for arg in node.args.args:
                variables.append(arg.arg)
        elif node.__class__.__name__ == "For":
            variables += get_variables(node.target)
            variables += get_variables(node.iter)
        else:
            print_details(node)
            variables = get_all_possible_operators(node, variables)

        for subnode in node.body:
            variables += get_variables(subnode)
    elif isinstance(node, _ast.BinOp):
        variables += get_variables(node.left)
        variables += get_variables(node.right)
    elif isinstance(node, _ast.Assign):
        for name in node.targets:
            if isinstance(name, _ast.Name):
                variables.append(name.id)
            else:
                variables += get_variables(name)
        variables += get_variables(node.value)
    elif node.__class__.__name__ == "Constant":
        variables.append(node.value)
    elif node.__class__.__name__ == "Call":  # node.func.attr = split; node.func.value is name .value = point1
        for arg in node.args:
            variables += get_variables(arg)
    elif node.__class__.__name__ == "UnaryOp":
        # variables.append(node.op.__class__.__name__ + str(node.operand.value))
        variables += get_variables(node.operand)
    elif node.__class__.__name__ == "Expr":
        variables += get_variables(node.value)
    elif node.__class__.__name__ == "Return":
        variables += get_variables(node.value)
    elif node.__class__.__name__ == "Name":
        variables.append(node.id)
    elif node.__class__.__name__ == "Subscript":
        variables += get_variables(node.slice)
        variables += get_variables(node.value)
    elif node.__class__.__name__ == "AugAssign":
        variables += get_variables(node.target)
        variables += get_variables(node.value)
    elif node.__class__.__name__ == "Dict":
        for key in node.keys:
            variables += get_variables(key)
        for value in node.values:
            variables += get_variables(value)
    elif node.__class__.__name__ == "Global":
        for name in node.names:
            variables.append(name)
    # elif node.__class__.__name__ == "Tuple":

    else:
        print_details(node)
        variables = get_all_possible_operators(node, variables)
    return variables


def print_details(node):
    if node.__class__.__name__ not in solved and hasattr(node, 'lineno'):
        print("Word left for (" + str(node.lineno) + "): " + node.__class__.__name__)
    elif node.__class__.__name__ not in solved:
        print("Word left for (" + "): " + node.__class__.__name__)


def get_all_possible_operators(node, variables):
    if node is not None:
        if not hasattr(node, '__dict__'):
            variables.append(node)
            return variables

        keys = node.__dict__.keys()
        for key in keys:
            if key in ["body", "lineno", "col_offset", "end_lineno", "end_col_offset", "ctx", "dims"]:
                continue
            elif isinstance(getattr(node, key), list):
                for item in getattr(node, key):
                    variables += get_variables(item)
            else:
                variables += get_variables(getattr(node, key))
    return variables


def get_function_nodes(node):
    functions = []
    if hasattr(node, 'body'):
        for subNode in node.body:
            if subNode.__class__.__name__ == "FunctionDef":
                functions.append(subNode)

    return functions


def is_block_comment(node):
    return node.__class__.__name__ == "Expr" and node.value.__class__.__name__ == "Constant"


def main():
    all_file_names = ["knn.py"]
    # all_file_names = ["F:\\IIT\\Projects\\PyProj\\alg_toolbox4\\combinatorics\\main.py"]
    file_count = 0
    for file_name in all_file_names:
        if "venv" not in file_name and "__init__.py" not in file_name and "env" not in file_name:
            file_count += 1
            print("File number {}".format(file_count))
            try:
                file = open(file_name).read()
                print(file_name)
                nodes = ast.parse(file)
                functions = get_function_nodes(nodes)
                func_count = 0

                for function in functions:
                    func_count += 1
                    vars = get_variables(function)
                    print(str(func_count) + ". Function " + function.name + ": ")
                    print(vars)
            except UnicodeDecodeError:
                print("Skipping " + file_name)


main()
