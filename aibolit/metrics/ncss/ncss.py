# The MIT License (MIT)
#
# Copyright (c) 2020 Aibolit
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from networkx import dfs_labeled_edges  # type: ignore

from aibolit.utils.ast_builder import build_ast
from aibolit.ast_framework import AST, ASTNodeType


class NCSSMetric():
    def __init__(self):
        pass

    def value(self, filename: str):
        set_of_the_types = {ASTNodeType.ANNOTATION_DECLARATION,
                            ASTNodeType.CLASS_DECLARATION,
                            ASTNodeType.CONSTANT_DECLARATION,
                            ASTNodeType.CONSTRUCTOR_DECLARATION,
                            ASTNodeType.DECLARATION,
                            ASTNodeType.ENUM_CONSTANT_DECLARATION,
                            ASTNodeType.ENUM_DECLARATION,
                            ASTNodeType.FIELD_DECLARATION,
                            ASTNodeType.INTERFACE_DECLARATION,
                            ASTNodeType.LOCAL_VARIABLE_DECLARATION,
                            ASTNodeType.METHOD_DECLARATION,
                            ASTNodeType.TYPE_DECLARATION,
                            ASTNodeType.VARIABLE_DECLARATION,
                            ASTNodeType.CATCH_CLAUSE,
                            ASTNodeType.ASSERT_STATEMENT,
                            ASTNodeType.BREAK_STATEMENT,
                            ASTNodeType.CONTINUE_STATEMENT,
                            ASTNodeType.DO_STATEMENT,
                            ASTNodeType.FOR_STATEMENT,
                            ASTNodeType.IF_STATEMENT,
                            ASTNodeType.RETURN_STATEMENT,
                            ASTNodeType.STATEMENT,
                            ASTNodeType.STATEMENT_EXPRESSION,
                            ASTNodeType.SWITCH_STATEMENT,
                            ASTNodeType.SWITCH_STATEMENT_CASE,
                            ASTNodeType.SYNCHRONIZED_STATEMENT,
                            ASTNodeType.THROW_STATEMENT,
                            ASTNodeType.TRY_STATEMENT,
                            ASTNodeType.WHILE_STATEMENT}

        if len(filename) == 0:
            raise ValueError('Empty file for analysis')

        tree = AST.build_from_javalang(build_ast(filename))
        metric = 0
        for _, destination, edge_type in dfs_labeled_edges(tree.tree, tree.root):
            if edge_type == 'forward':
                node_type = tree.get_type(destination)
                if node_type in set_of_the_types:
                    metric += 1
                if node_type == ASTNodeType.FOR_CONTROL:
                    metric -= len(list(tree.children_with_type(destination, ASTNodeType.VARIABLE_DECLARATION)))
                    metric -= len(list(tree.children_with_type(destination, ASTNodeType.LOCAL_VARIABLE_DECLARATION)))

        return metric
