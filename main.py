import ast
import _ast
import glob

# all_file_names = glob.glob("F:\\IIT\\Projects\\PyProj" + "/**/*.py", recursive=True)
solved = ["If", "Compare", "Eq", "List", "Tuple", "IsNot", "Gt", "Lt", "NoneType", "Slice"]
comments = []
file_in_lines = []
temp = set()


def get_block_comment(node):
    comments = []
    if is_block_comment(node):
        comments.append({
            "lineNo": node.lineno,
            "endLineNo": node.end_lineno
        })
        return comments

    if hasattr(node, 'body'):
        for subnode in node.body:
            comments += get_block_comment(subnode)

    return comments


def get_operands(node, parent_node=None):
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
        if hasattr(node, "func") and hasattr(node.func, "value"):
            variables += get_operands(node.func.value)
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
            string = file_in_lines[node.lineno - 1][node.col_offset:node.end_col_offset]
            item = {
                "lineno": node.lineno - 1,
                "end_lineno": node.end_lineno,
                "col_offset": node.col_offset + string.find(name),
                "end_col_offset": node.col_offset + string.find(name) + len(name),
                "value": name
            }
            variables.append(item)
            assert str(file_in_lines[node.lineno - 1][item["col_offset"]:item["end_col_offset"]]) == str(item['value'])
    # elif node.__class__.__name__ == "Tuple":

    else:
        # print_details(node)
        variables = get_all_possible_operators(node, variables, parent_node)
    return variables


def get_node_detail_obj(node, value=None):
    item = {
        "lineno": node.lineno - 1,
        "end_lineno": node.end_lineno,
        "col_offset": node.col_offset - 1,
        "end_col_offset": node.end_col_offset
    }
    if value is not None:

        value = str(value).replace("\\", "\\\\")
        value = str(value).replace("\n", "\\n")

        string = file_in_lines[node.lineno - 1][node.col_offset:node.end_col_offset]
        item = {
            "lineno": node.lineno - 1,
            "end_lineno": node.end_lineno,
            "col_offset": node.col_offset + string.find(str(value)),
            "end_col_offset": node.col_offset + string.find(str(value)) + len(str(value)),
            "value": value
        }
        if not is_float(value):
            assert str(file_in_lines[node.lineno - 1][item["col_offset"]:item["end_col_offset"]]) == str(value)
    return item


def is_float(fl):
    try:
        float(fl)
        return True
    except ValueError:
        return False


def print_details(node):
    if node.__class__.__name__ not in solved and hasattr(node, 'lineno'):
        print("Word left for (" + str(node.lineno) + "): " + node.__class__.__name__)
    elif node.__class__.__name__ not in solved:
        print("Word left for (" + "): " + node.__class__.__name__)


def get_all_possible_operators(node, variables, parent_node=None):
    if node is not None:
        if not hasattr(node, '__dict__'):
            # variables.append(node)
            string = file_in_lines[parent_node.lineno - 1][parent_node.col_offset:parent_node.end_col_offset]
            item = {
                "lineno": parent_node.lineno - 1,
                "end_lineno": parent_node.end_lineno,
                "col_offset": parent_node.col_offset + string.find(node),
                "end_col_offset": parent_node.col_offset + string.find(node) + len(node),
                "value": node
            }
            variables.append(item)
            assert str(file_in_lines[parent_node.lineno - 1][item["col_offset"]:item["end_col_offset"]]) == str(
                item['value'])
            return variables

        keys = node.__dict__.keys()
        for key in keys:
            if key in ["body", "lineno", "col_offset", "end_lineno", "end_col_offset", "ctx", "dims", "is_async",
                       "conversion"]:
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


def remove_comment(block_comment, lines):
    
    for comment in block_comment:        
        for x in range(comment['lineNo'], comment['endLineNo']+1):
            lines[x-1] = " \n"

    return lines


def print_lines(lines):
    count = 0
    for line in lines:
        count += 1
        print("Line{}: {}".format(count, line))


def remove_single_comment(lines):
    
    counter = 0
    for line in lines:
        lines[counter] = line.split('#')[0] + "\n"
        counter += 1
    return lines
# b[:4] + b[7+1:]

def remove_operands(lines, operands):
    
    for var in operands:
        line_no = var['lineno']
        # start_index = var['col_offset']
        # end_index = var['end_col_offset']
        
        lines[line_no] = lines[line_no].replace(var['value'], '')
    
    # print_lines(lines)
    
    return lines


def insert_operators(lines):
    list_of_operators = []
    
    return list_of_operators
    

def get_operators(node, lines, operands):
    operators = []
    block_comment = get_block_comment(node)
    # print(block_comment)

    if len(block_comment) > 0:
        lines = remove_comment(block_comment, lines)

    # print("*****Comment Removed*****")
    # print_lines(lines)

    lines = remove_operands(lines, operands)
    


def main():
    all_file_names = ["test.py"]
    # all_file_names = ["F:\\IIT\\Projects\\PyProj\\alg_toolbox4\\week_4\\closest_points.py"]
    file_count = 0
    for file_name in all_file_names:
        if is_not_lib_file(file_name):
            file_count += 1
            # print("File number {}".format(file_count))
            try:
                file = open(file_name).read()
                global file_in_lines
                file_in_lines = file.split("\n")
                print(file_name)
                nodes = ast.parse(file)
                functions = get_function_nodes(nodes)
                func_count = 0
                
                lines_without_single_line_comment = remove_single_comment(file_in_lines)
                print(lines_without_single_line_comment)

                for function in functions:
                    func_count += 1
                    vars = get_operands(function)
                    # print(function.lineno, function.end_lineno)
                    print(str(func_count) + ". Function " + function.name + ": ")
                    # print(vars)
                    vars.sort(key=lambda x: (x['lineno'], -x['end_col_offset']))
                    # print("***********Sorted**********")
                    # print(vars)
                    
                    get_operators(function, lines_without_single_line_comment, vars)
                    
                print_lines(lines_without_single_line_comment)

            except UnicodeDecodeError:
                print("Skipping " + file_name)


def is_not_lib_file(file_name):
    list = ["venv", "__init__.py", "env", "BCCB", "flask", "manage.py"]

    for item in list:
        if item in file_name:
            return False
    return True


main()
print(temp)
