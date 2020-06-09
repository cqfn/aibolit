from aibolit.utils.ast_builder import build_ast
from javalang.tree import VariableDeclarator, ConstructorDeclaration


class NumVars:
    '''
    This class count number of methods and variables in class
    input: filename
    output: number of variables
    '''
    def __init__(self):
        pass

    def value(self, filename: str) -> int:
        tree = build_ast(filename)
        count_variables = 0
        # for variables defined as the arguments of method
        for _, var_body in tree.filter(ConstructorDeclaration):
            if hasattr(var_body, 'parameters'):  # type: ignore
                check_params = var_body.parameters  # type: ignore
                if len(check_params) != 0:
                    for _ in check_params:
                        count_variables += 1
        # for other unique variables
        count_variables += sum([1 for _, var_body in tree.filter(VariableDeclarator)])
        return count_variables