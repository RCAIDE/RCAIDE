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
                self.assignments.append(('Subscript Assignment', ast.unparse(node), node.lineno))
        self.generic_visit(node)

    def visit_AugAssign(self, node):
        if isinstance(node.target, ast.Subscript):
            self.assignments.append(('Augmented Assignment', ast.unparse(node), node.lineno))
        elif isinstance(node.target, ast.Name):
            self.assignments.append(('Augmented Assignment', ast.unparse(node), node.lineno))
        self.generic_visit(node)

def find_assignments(file_path):
    with open(file_path, 'r') as file:
        tree = ast.parse(file.read())

    finder = SubscriptAssignmentFinder()
    finder.visit(tree)
    return finder.assignments

def process_directory(directory):
    total_matches = 0
    subdirectory_matches = defaultdict(int)

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                assignments = find_assignments(file_path)
                if assignments:
                    print(f"File: {file_path}")
                    for assignment_type, assignment, line_number in assignments:
                        print(f"  Line {line_number}: {assignment_type}: {assignment}")
                    print(f"  Total matches in this file: {len(assignments)}")
                    print()

                    total_matches += len(assignments)
                    subdirectory_matches[os.path.dirname(file_path)] += len(assignments)

    print("Matches per subdirectory:")
    for subdir, count in subdirectory_matches.items():
        print(f"  {subdir}: {count}")

    print(f"\nTotal matches overall: {total_matches}")

if __name__ == "__main__":
    directory = Path('./RCAIDE/')
    process_directory(directory)
    