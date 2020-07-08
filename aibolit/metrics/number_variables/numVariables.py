from aibolit.utils.ast_builder import build_ast

from javalang.tree import VariableDeclarator, MemberReference


class NumVars:
    '''
    This class count number variables in class
    input: filename
    output: number of variables
    '''
    def __init__(self):
        pass

    def value(self, filename: str) -> int:
        tree = build_ast(filename)
        count_variables = set()
        for _, var_body in tree.filter(VariableDeclarator):
            count_variables.add(var_body.name)

        for _, var_body1 in tree.filter(MemberReference):
            count_variables.add(var_body1.member)

        return len(count_variables)
