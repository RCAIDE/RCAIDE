import ast
import os
from pathlib import Path

class SubscriptAssignmentFinder(ast.NodeVisitor):
    def __init__(self):
        self.subscript_assignments = []

    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Subscript):
                self.subscript_assignments.append(ast.unparse(node))
        self.generic_visit(node)


def find_subscript_assignments(file_path):
    with open(file_path, 'r') as file:
        tree = ast.parse(file.read())
    
    finder = SubscriptAssignmentFinder()
    finder.visit(tree)
    return finder.subscript_assignments


def process_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                assignments = find_subscript_assignments(file_path)
                if assignments:
                    print(f"File: {file_path}")
                    for assignment in assignments:
                        print(f"  {assignment}")
                    print()


if __name__ == "__main__":
    directory = Path('./Legacy/trunk/S/Methods/Aerodynamics/Common/Fidelity_Zero/Lift')
    process_directory(directory)