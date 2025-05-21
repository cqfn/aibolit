# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT
from typing import List

from aibolit.ast_framework import ASTNodeType, AST


class ErClass:
    '''
    Check if a class name include the forbidden word
    '''
    forbiden_words_in_class_names = (
        'manager',
        'controller',
        'router',
        'dispatcher',
        'printer',
        'writer',
        'reader',
        'parser',
        'generator',
        'renderer',
        'listener',
        'producer',
        'holder',
        'interceptor')

    def value(self, ast: AST) -> List[int]:
        lines: List[int] = []
        for node in ast.get_proxy_nodes(ASTNodeType.CLASS_DECLARATION):
            class_name = node.name.lower()
            if any(forbiden_word in class_name
                   for forbiden_word in self.forbiden_words_in_class_names):
                lines.append(node.line)
        return lines
