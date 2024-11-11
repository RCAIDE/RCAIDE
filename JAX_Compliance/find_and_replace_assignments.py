import ast, os, fileinput, termios, sys, tty



class SubscriptAssignmentFinder(ast.NodeVisitor):
    def __init__(self):
        self.assignments = []

    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Subscript):
                if self.is_boolean_indexing(target.slice):
                    self.assignments.append(('Boolean Indexing', ast.unparse(node), node.lineno))
                else:
                    self.assignments.append(('Subscript Assignment', ast.unparse(node), node.lineno))
        self.generic_visit(node)

    def visit_AugAssign(self, node):
        if isinstance(node.target, ast.Subscript):
            if self.is_boolean_indexing(node.target.slice):
                self.assignments.append(('Boolean Indexing', ast.unparse(node), node.lineno))
            else:
                self.assignments.append(('Augmented Assignment', ast.unparse(node), node.lineno))
        elif isinstance(node.target, ast.Name):
            self.assignments.append(('Augmented Assignment', ast.unparse(node), node.lineno))
        self.generic_visit(node)

    def is_boolean_indexing(self, slice_node):
        return isinstance(slice_node, ast.Index) and isinstance(slice_node.value, (ast.Compare, ast.BoolOp))


def process_file(file_path):
    with open(file_path, 'r') as file:
        tree = ast.parse(file.read())

    finder = SubscriptAssignmentFinder()
    finder.visit(tree)

    jax_dict = {
        '+': 'add',
        '-': 'subtract',
        '*': 'multiply',
        '/': 'divide',
        '**': 'power'
    }

    for assignment_type, code, line_number in finder.assignments:
        print(f"\nFile: {file_path}")
        print(f"Line {line_number}: {assignment_type}")
        print(f"Current Version:\n\t{code}")

        if assignment_type == 'Boolean Indexing' or assignment_type == 'Subscript Assignment':
            lhs, rhs = code.split('=', 1)
            jax_code = f"{lhs.strip()} = {lhs.strip()}.at[{lhs.split('[')[1].split(']')[0]}].set({rhs.strip()})"
        elif assignment_type == 'Augmented Assignment':
            lhs, op, rhs = code.split(' ', 2)
            lhs = lhs.strip().split('[')
            op = op[:-1]  # Remove the '='
            if op in jax_dict:
                if len(lhs) > 1:
                    var = lhs[0].strip()
                    idx = lhs[1].split(']')[0]

                else:
                    var = lhs[0].strip()
                    idx = ':'
                jax_code = f"{var} = {var}.at[{idx}].{jax_dict[op]}({rhs.strip()})"
        else:
            jax_code = code  # No change for other types

        print(f"JAX-compliant:\n\t{jax_code}")

        def get_input():
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                return ch

        print("Apply change? (Yes: J / No: K / Flag: L)")
        choice = get_input().lower()
        if choice == 'j':
            apply_change(file_path, line_number, code, jax_code)
        elif choice == 'l':
            flag_for_review(file_path, line_number)


def apply_change(file_path, line_number, old_code, new_code):
    for line in fileinput.input(file_path, inplace=True):
        if fileinput.filelineno() == line_number and old_code in line:
            print(line.replace(old_code, new_code), end='')
        else:
            print(line, end='')


def flag_for_review(file_path, line_number):
    for line in fileinput.input(file_path, inplace=True):
        if fileinput.filelineno() == line_number:
            print(f"{line.rstrip()}  #TODO: requires manual review")
        else:
            print(line, end='')


def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                process_file(os.path.join(root, file))


if __name__ == "__main__":
    process_directory('/home/jordan/dev/ARC/RCAIDE/RCAIDE/Framework/Mission/Functions/Initialize')
