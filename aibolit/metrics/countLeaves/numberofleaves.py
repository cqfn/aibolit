# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT
import os
from typing import Any, List

import javalang
import javalang.tree
from javalang.ast import Node

from aibolit.utils.ast_builder import build_ast


class CountNumberOfLeaves:
    """
    Returns number of leaves in class (sum by each method).
    input: file_path
    output: sum of leaves in class by each method
    """
    def __init__(self):
        pass

    def countLeaves(self, root: Node | list[Node]) -> int:
        # forming the same data type for each object
        root_arr = root if isinstance(root, List) else [root]
        leaves = 0
        not_count: List[Any] = [None, '', set()]

        # traverse through all childs of object. If there is no child, hence we faced leaf
        for node in root_arr:

            if not hasattr(node, 'children') and node not in not_count:
                return leaves + 1

            elif node in not_count:
                continue

            for each_child in node.children:
                leaves += self.countLeaves(each_child)

        return leaves

    def value(self, filename: str | os.PathLike) -> int:

        tree = build_ast(filename)
        traversed = []
        for _, class_body in tree.filter(javalang.tree.ClassDeclaration):
            for each_object in class_body.body:
                if isinstance(each_object, javalang.tree.MethodDeclaration):
                    traversed.append(self.countLeaves(each_object.body))

        return sum(traversed)
