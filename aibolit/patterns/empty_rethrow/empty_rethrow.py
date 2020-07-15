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
from aibolit.ast_framework import ASTNodeType, AST
from aibolit.utils.ast_builder import build_ast
from typing import List, Set


class EmptyRethrow:
    '''
    Check if we throw the same exception as it was caught
    '''

    def value(self, filename) -> List[int]:
        total_code_lines: Set[int] = set()
        ast = AST.build_from_javalang(build_ast(filename))
        for try_node in ast.get_proxy_nodes(ASTNodeType.TRY_STATEMENT):
            for throw_node in ast.get_proxy_nodes(ASTNodeType.THROW_STATEMENT):
                field_catche = try_node.catches
                if field_catche:
                    catch_classes = [x.parameter.name for x in field_catche]
                    throw_child = list(throw_node.children)[0]
                    if throw_child.node_type == ASTNodeType.CLASS_CREATOR:
                        continue
                    if hasattr(throw_child, 'member') and throw_child.member in catch_classes:
                            total_code_lines.add(throw_child.line)
        return sorted(total_code_lines)
