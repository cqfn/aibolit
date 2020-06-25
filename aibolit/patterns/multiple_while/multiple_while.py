from aibolit.utils.ast import AST, ASTNodeType
from aibolit.utils.ast_builder import build_ast


class MultipleWhile:

    def __init__(self):
        pass

    def value(self, filename: str):
        """
        Travers over AST tree and finds function with sequential while statement
        :param filename:
        :return:
        List of LineNumber of methods which have sequential while statements
        """

        tree = AST(build_ast(filename))
        res = []
        nodes = tree.nodes_by_type(ASTNodeType.METHOD_DECLARATION)
        for node in nodes:
            cur_line = tree.get_attr(node, 'source_code_line')
            while_cyclo = tree.all_children_with_type(node, ASTNodeType.WHILE_STATEMENT)
            count = 0
            for cyclo in while_cyclo:
                count += 1
                if count > 1:
                    res.append(cur_line)
                    break

        return res
