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

from unittest import TestCase
from pathlib import Path
from networkx import dfs_preorder_nodes

from aibolit.utils.ast_builder import build_ast
from aibolit.utils.ast import AST, ASTNodeType


class ASTTestSuite(TestCase):
    def test_parsing_with_preorder_traversal(self):
        for filename, ast_preordered_traversed in \
                ASTTestSuite._java_source_code_filename_to_ast_preordered_traversed:

            with self.subTest('Parsing {}'.format(filename)):
                javalang_ast = build_ast(Path(__file__).parent.absolute() / filename)
                ast = AST(javalang_ast)
                self.assertEqual([ast.tree.nodes[node_index]['type']
                                  for node_index in dfs_preorder_nodes(ast.tree, ast.root)],
                                 ast_preordered_traversed)

    _java_source_code_filename_to_ast_preordered_traversed = \
        [
            ('simple_class.java', [
                ASTNodeType.COMPILATION_UNIT,
                ASTNodeType.CLASS_DECLARATION,
                ASTNodeType.COLLECTION,
                ASTNodeType.STRING,
                ASTNodeType.FIELD_DECLARATION,
                ASTNodeType.COLLECTION,
                ASTNodeType.STRING,
                ASTNodeType.BASIC_TYPE,
                ASTNodeType.STRING,
                ASTNodeType.VARIABLE_DECLARATOR,
                ASTNodeType.STRING,
                ASTNodeType.LITERAL,
                ASTNodeType.STRING,
                ASTNodeType.METHOD_DECLARATION,
                ASTNodeType.COLLECTION,
                ASTNodeType.STRING,
                ASTNodeType.BASIC_TYPE,
                ASTNodeType.STRING,
                ASTNodeType.STRING,
                ASTNodeType.STATEMENT_EXPRESSION,
                ASTNodeType.ASSIGNMENT,
                ASTNodeType.MEMBER_REFERENCE,
                ASTNodeType.STRING,
                ASTNodeType.STRING,
                ASTNodeType.LITERAL,
                ASTNodeType.STRING,
                ASTNodeType.STRING,
                ASTNodeType.RETURN_STATEMENT,
                ASTNodeType.MEMBER_REFERENCE,
                ASTNodeType.STRING,
                ASTNodeType.STRING,
            ])
        ]
