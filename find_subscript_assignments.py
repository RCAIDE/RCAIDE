import ast
import os
from pathlib import Path
from collections import defaultdict

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
        if isinstance(slice_node, ast.Index):
            # For Python 3.8 and earlier
            slice_value = slice_node.value
        else:
            # For Python 3.9+
            slice_value = slice_node

        return (
            isinstance(slice_value, ast.Compare) or
            (isinstance(slice_value, ast.BinOp) and isinstance(slice_value.op, (ast.And, ast.Or))) or
            (isinstance(slice_value, ast.UnaryOp) and isinstance(slice_value.op, ast.Not))
        )

def find_assignments(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        tree = ast.parse(file.read())

    finder = SubscriptAssignmentFinder()
    finder.visit(tree)
    return finder.assignments

def process_directory(directory, print_console=True, save_file=False, output_file=None):
    total_matches = 0
    subdirectory_matches = defaultdict(int)

    def write_output(message):
        if print_console:
            print(message)
        if save_file:
            file_handle.write(message + "\n")

    file_handle = open(output_file, 'w', encoding='utf-8') if save_file else None

    try:
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    assignments = find_assignments(file_path)
                    if assignments:
                        write_output(f"File: {file_path}")
                        for assignment_type, assignment, line_number in assignments:
                            write_output(f"  Line {line_number}: {assignment_type}: {assignment}")
                        write_output(f"  Total matches in this file: {len(assignments)}")
                        write_output("")

                        total_matches += len(assignments)
                        subdirectory_matches[os.path.dirname(file_path)] += len(assignments)

        write_output("Matches per subdirectory:")
        for subdir, count in subdirectory_matches.items():
            write_output(f"  {subdir}: {count}")

        write_output(f"\nTotal matches overall: {total_matches}")

    finally:
        if file_handle:
            file_handle.close()

    if save_file:
        print(f"Results have been saved to {output_file}")


if __name__ == "__main__":
    directories = [Path('./RCAIDE/Framework'),
                   Path('./RCAIDE/Library/Attributes'),
                   Path('./RCAIDE/Library/Components'),
                   Path('./RCAIDE/Library/Methods/Aerodynamics'),
                   Path('./RCAIDE/Library/Methods/Geometry'),
                   Path('./RCAIDE/Library/Methods/Propulsors'),
                   Path('./RCAIDE/Library/Methods/Stability')]
    output_file = "subscript_assignments.txt"

    directory_handles = ['framework', 'attributes', 'components', 'aerodynamics', 'geometry', 'propulsors', 'stability']

    # Example usage:
    # To print to console only:
    # process_directory(directories[0], print_console=True, save_file=False)

    # To save to file only:
    # process_directory(directories[0], print_console=False, save_file=True, output_file=output_file)

    # To print to console and save to file:
    # process_directory(directories[0], print_console=True, save_file=True, output_file=output_file)

    # To neither print to console nor save to file (just process without output):
    # process_directory(directories[0], print_console=False, save_file=False)

    for idx, d in enumerate(directories):
        process_directory(d,
                          print_console=True,
                          save_file=True,
                          output_file=directory_handles[idx]+"_subscript_assignments.txt")
