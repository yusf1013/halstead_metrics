import ast
import _ast
import glob

all_file_names = glob.glob("F:\\IIT\\Projects\\PyProj" + "/**/*.py", recursive=True)
solved = ["If", "Compare", "Eq", "List", "Tuple", "IsNot", "Gt", "Lt", "NoneType", "Slice"]
comments = []
file_in_lines = []
temp = set()


def get_operands(node, parent_node = None):
    variables = []

    if is_block_comment(node):
        comments.append(get_node_detail_obj(node))
        return variables

    if hasattr(node, 'body'):
        if node.__class__.__name__ == "FunctionDef":
            for arg in node.args.args:
                variables.append(get_node_detail_obj(arg, arg.arg))
        elif node.__class__.__name__ == "For":
            variables += get_operands(node.target)
            variables += get_operands(node.iter)
        else:
            print_details(node)
            variables = get_all_possible_operators(node, variables)

        for subnode in node.body:
            variables += get_operands(subnode)
    elif isinstance(node, _ast.BinOp):
        variables += get_operands(node.left)
        variables += get_operands(node.right)
    elif isinstance(node, _ast.Assign):
        for name in node.targets:
            if isinstance(name, _ast.Name):
                variables.append(get_node_detail_obj(name, name.id))
            else:
                variables += get_operands(name)
        variables += get_operands(node.value)
    elif node.__class__.__name__ == "Constant":
        variables.append(get_node_detail_obj(node, node.value))
    elif node.__class__.__name__ == "Call":  # node.func.attr = split; node.func.value is name .value = point1
        for arg in node.args:
            variables += get_operands(arg)
    elif node.__class__.__name__ == "UnaryOp":
        variables += get_operands(node.operand)
    elif node.__class__.__name__ == "Expr":
        variables += get_operands(node.value)
    elif node.__class__.__name__ == "Return":
        variables += get_operands(node.value)
    elif node.__class__.__name__ == "Name":
        variables.append(get_node_detail_obj(node, node.id))
    elif node.__class__.__name__ == "Subscript":
        variables += get_operands(node.slice)
        variables += get_operands(node.value)
    elif node.__class__.__name__ == "AugAssign":
        variables += get_operands(node.target)
        variables += get_operands(node.value)
    elif node.__class__.__name__ == "Dict":
        for key in node.keys:
            variables += get_operands(key)
        for value in node.values:
            variables += get_operands(value)
    elif node.__class__.__name__ == "Global":
        for name in node.names:
            str = file_in_lines[node.lineno-1][node.col_offset-1:node.end_col_offset]
            variables.append({
                "lineno": node.lineno - 1,
                "end_lineno": node.end_lineno,
                "col_offset": node.col_offset-1+str.find(name),
                "end_col_offset": node.col_offset-1+str.find(name)+len(name),
                "value": name
            })
    # elif node.__class__.__name__ == "Tuple":

    else:
        print_details(node)
        variables += get_all_possible_operators(node, variables, parent_node)
    return variables




def get_node_detail_obj(node, value=None):
    item = {
        "lineno": node.lineno - 1,
        "end_lineno": node.end_lineno,
        "col_offset": node.col_offset - 1,
        "end_col_offset": node.end_col_offset
    }
    if value is not None:
        item['value'] = value
    return item


def print_details(node):
    if node.__class__.__name__ not in solved and hasattr(node, 'lineno'):
        print("Word left for (" + str(node.lineno) + "): " + node.__class__.__name__)
    elif node.__class__.__name__ not in solved:
        print("Word left for (" + "): " + node.__class__.__name__)


def get_all_possible_operators(node, variables, parent_node=None):
    if node is not None:
        if not hasattr(node, '__dict__'):
            # variables.append(node)
            str = file_in_lines[parent_node.lineno-1][parent_node.col_offset-1:parent_node.end_col_offset]
            variables.append({
                "lineno": parent_node.lineno - 1,
                "end_lineno": parent_node.end_lineno,
                "col_offset": parent_node.col_offset - 1 + str.find(node),
                "end_col_offset": parent_node.col_offset - 1 + str.find(node) + len(node),
                "value": node
            })
            return variables

        keys = node.__dict__.keys()
        for key in keys:
            if key in ["body", "lineno", "col_offset", "end_lineno", "end_col_offset", "ctx", "dims", "is_async"]:
                continue
            elif isinstance(getattr(node, key), list):
                for item in getattr(node, key):
                    variables += get_operands(item)
            else:
                variables += get_operands(getattr(node, key), node)
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
    # all_file_names = ["F:\\IIT\\Projects\\PyProj\\alg_toolbox4\\week_4\\closest_points.py"]
    file_count = 0
    for file_name in all_file_names:
        if "venv" not in file_name and "__init__.py" not in file_name and "env" not in file_name:
            file_count += 1
            print("File number {}".format(file_count))
            try:
                file = open(file_name).read()
                global file_in_lines
                file_in_lines = file.split("\n")
                print(file_name)
                nodes = ast.parse(file)
                functions = get_function_nodes(nodes)
                func_count = 0

                for function in functions:
                    func_count += 1
                    vars = get_operands(function)
                    print(str(func_count) + ". Function " + function.name + ": ")
                    print(vars)
            except UnicodeDecodeError:
                print("Skipping " + file_name)


main()
print(temp)
