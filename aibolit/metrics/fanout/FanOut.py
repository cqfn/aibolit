from aibolit.utils.ast_builder import build_ast
from javalang.tree import ClassCreator, ClassDeclaration, MethodInvocation, VariableDeclarator


class FanOut:
    '''
    Fan Out metric is defined as the number of other classes referenced by a class.
    '''
    def __init__(self):
        pass

    def value(self, filename: str) -> int:
        considered_classes = {'System.out': 0}
        fan_outs = 0
        tree = build_ast(filename)
        # to not increment java.util classes
        for import_ in tree.imports:
            if import_.path.startswith('java.util'):
                considered_classes[import_.path.split('.')[-1]] = 0

        for _, class_body in tree.filter(ClassDeclaration):
            for _, declaration in class_body.filter(VariableDeclarator):
                if type(declaration.initializer) == ClassCreator:
                    if considered_classes.get(declaration.initializer.type.name) is None:
                        considered_classes[declaration.initializer.type.name] = 0
                        considered_classes[declaration.name] = 0
                        fan_outs += 1

            for _, external_method in class_body.filter(MethodInvocation):
                if considered_classes.get(external_method.qualifier) is None:
                    considered_classes[external_method.qualifier] = 0
                    fan_outs += 1

        return fan_outs
