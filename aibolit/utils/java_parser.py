# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

import javalang.tree

# mapping between javalang node class names and Java keywords
NODE_KEYWORD_MAP = {
    'SuperMethodInvocation': 'super',
    'WhileStatement': 'while',
    'ForStatement': 'for',
    'TryStatement': 'try',
    'CatchClause': 'catch',
    'SynchronizedStatement': 'synchronized'
}

# list of nodes creating new scope
NEW_SCOPE_NODES = [
    javalang.tree.MethodDeclaration,
    javalang.tree.IfStatement,
    javalang.tree.ForStatement,
    javalang.tree.SwitchStatement,
    javalang.tree.TryStatement,
    javalang.tree.DoStatement,
    javalang.tree.WhileStatement,
    javalang.tree.BlockStatement,
    javalang.tree.CatchClause,
    javalang.tree.SynchronizedStatement
]


class ASTNode:
    def __init__(self, line, method_line, node, scope):
        self.line = line  # node line number in the file
        self.method_line = method_line  # line number where parent method declared
        self.node = node  # javalang AST node object
        self.scope = scope  # ID of scope this node belongs
