import os
import ast
import re
import tokenize
from io import BytesIO
from collections import namedtuple
from pathlib import Path

def add_framework_methods(old_folder_path, new_folder_path):

    for root, _, files in os.walk(old_folder_path):

        for file in files:
            if file.endswith('.py'):
                if file == '__init__.py':
                    continue
                else:
                    abs_file_path = os.path.join(root, file)
                    rel_file_path = os.path.join(os.path.relpath(root, old_folder_path), file)
                    RCAIDE_file_source = create_RCAIDE_method_source(abs_file_path)
                    RCAIDE_file_name = new_folder_path+'/'+rel_file_path
                    RCAIDE_file = Path(RCAIDE_file_name)
                    RCAIDE_file.parent.mkdir(parents=True, exist_ok=True)
                    with open(RCAIDE_file_name, 'w+') as RC_file:
                        RC_file.write(RCAIDE_file_source)




def create_RCAIDE_method_source(file_path):

    with open(file_path, 'r') as file:
        source = file.read()

    try:
        tree = ast.parse(source)
    except SyntaxError:
        print(f"Skipping {file_path} due to syntax errors.")
        return

    functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]

    modified_source = source

    for function in functions:

        old_name = function.name
        new_name = f'func_{old_name}'

        modified_source = re.sub(r'\bdef\s+%s\b' % re.escape(old_name),
                                 'def %s' % new_name,
                                 modified_source)

        framework_function_source = f'{old_name}(State, Settings, System):\n'

        unpack_string = ''
        primal_args = [arg.arg for arg in function.args.args]
        primal_kwargs = [kwarg.arg for kwarg in function.args.kwonlyargs]
        try:
            max_arg_length = max([len(arg) for arg in primal_args] + [len(arg) for arg in primal_kwargs])
        except:
            max_arg_length = 1
        for arg in primal_args:
            unpack_string += f"\t#TODO: {arg: <{max_arg_length}} = [Replace With State, Settings, or System Attribute]\n"
        for kwarg in primal_kwargs:
            unpack_string += f"\t#TODO: {kwarg: <{max_arg_length}} = [Replace With State, Settings, or System Attribute]\n"

        call_string = f'\n\tresults = {new_name}{*primal_args,*primal_kwargs}\n'
        call_string += f"\t#TODO: [Replace results with the output of the original function]\n\n"

        pack_string = f'\tState, Settings, System = results\n'
        pack_string += f"\t#TODO: [Replace packing with correct attributes]\n\n"

        return_string = '\treturn State, Settings, System'

        framework_function_source += unpack_string + call_string + pack_string + return_string

        modified_source += '\n\n\n' + framework_function_source

    return modified_source

if __name__ == '__main__':
    old_folder_path = '/home/jordan/git/RCAIDE/Legacy/trunk/S/Methods'
    new_folder_path = 'home/jordan/git/RCAIDE/RCAIDE/Library/Methods'
    # old_folder_path = '/home/jordan/git/archAIDE/tests/frameworkConversionTest'
    # new_folder_path = '/home/jordan/git/archAIDE/tests/frameworkConversionTest_new'
    add_framework_methods(old_folder_path, new_folder_path)