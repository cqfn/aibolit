# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

import math
import os
import shutil
import subprocess
import tempfile
import uuid
from typing import Iterable

from bs4 import BeautifulSoup

from aibolit.ast_framework import AST, ASTNode, ASTNodeType


class NPathMetric():
    """Main NPath Complexity class."""

    input = ''

    def __init__(self, input):
        """Initialize class."""
        if len(input) == 0:
            raise ValueError('Empty file for analysis')
        self.input = input

    def value(self, showoutput=False):
        """Run NPath Complexity analaysis"""
        try:
            root = os.path.join(tempfile.gettempdir(), uuid.uuid4().hex)
            dirName = os.path.join(root, 'src/main/java')
            os.makedirs(dirName)
            if os.path.isdir(self.input):
                shutil.copytree(self.input, os.path.join(dirName, self.input))
            elif os.path.isfile(self.input):
                pos1 = self.input.rfind('/')
                os.makedirs(f'{dirName}/{self.input[0:pos1]}')
                shutil.copyfile(self.input, os.path.join(dirName, self.input))
            else:
                raise Exception(' '.join(['File', self.input, 'does not exist']))
            tmppath = os.path.dirname(os.path.realpath(__file__))
            shutil.copyfile(os.path.join(tmppath, 'pom.xml'), f'{root}/pom.xml')
            shutil.copyfile(os.path.join(tmppath, 'npath.xml'), f'{root}/npath.xml')
            if showoutput:
                subprocess.run(['mvn', 'pmd:pmd'], cwd=root, check=True)
            else:
                subprocess.run(['mvn', 'pmd:pmd'], cwd=root, check=True,
                               stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL)
            if os.path.isfile(f'{root}/target/pmd.xml'):
                res = self.__parseFile(root)
                return res
            raise Exception(' '.join(['File', self.input, 'analyze failed']))
        finally:
            shutil.rmtree(root)

    def __parseFile(self, root):
        result = {'data': [], 'errors': []}
        content = []
        with open(f'{root}/target/pmd.xml', 'r', encoding='utf-8') as file:
            content = file.read()
            soup = BeautifulSoup(content, features='xml')
            files = soup.find_all('file')
            for file in files:
                out = file.violation.string
                name = file['name']
                pos1 = name.find(f'{root}/src/main/java/')
                pos1 = pos1 + len(f'{root}/src/main/java/')
                name = name[pos1:]
                s = 'NPath complexity of '
                pos1 = out.find(s)
                pos1 = pos1 + len(s)
                complexity = int(out[pos1:])
                result['data'].append({'file': name, 'complexity': complexity})
            errors = soup.find_all('error')
            for error in errors:
                name = error['filename']
                pos1 = name.find(f'{root}/src/main/java/')
                pos1 = pos1 + len(f'{root}/src/main/java/')
                name = name[pos1:]
                raise Exception(error['msg'])
        return result


class MvnFreeNPathMetric:
    """
    NPathMetric class, which computes NPathMetric without use of `mvn` process.
    """
    def __init__(self, ast: AST) -> None:
        self.ast = ast

    def value(self) -> int:
        return sum(
            self._method_npath(method)
            for method in self.ast.get_proxy_nodes(ASTNodeType.METHOD_DECLARATION)
        )

    def _method_npath(self, method_node: ASTNode) -> int:
        return self._node_npath(method_node.body)

    def _node_npath(self, node: ASTNode) -> int:
        if isinstance(node, list):
            return self._sequence_npath(node)

        if node.node_type == ASTNodeType.IF_STATEMENT:
            return self._if_npath(node)
        elif node.node_type == ASTNodeType.SWITCH_STATEMENT:
            return self._switch_npath(node)
        elif node.node_type == ASTNodeType.FOR_STATEMENT:
            return self._for_loop_npath(node)
        elif node.node_type == ASTNodeType.BINARY_OPERATION:
            return self._binary_expression_npath(node)
        else:
            return self._sequence_npath(node.children)

    def _sequence_npath(self, nodes: Iterable[ASTNode]) -> int:
        return math.prod((self._node_npath(child) for child in nodes))

    def _if_npath(self, node: ASTNode) -> int:
        condition_npath = self._node_npath(node.condition)
        then_npath = self._node_npath(node.then_statement)
        else_npath = (
            self._node_npath(node.else_statement)
            if node.else_statement is not None
            else 1
        )
        return condition_npath * (then_npath + else_npath)

    def _switch_npath(self, node: ASTNode) -> int:
        def _group_npath(case_group: ASTNode) -> int:
            return math.prod((self._node_npath(case) for case in case_group.children))

        case_paths = sum(_group_npath(case_group) for case_group in node.cases)
        return self._node_npath(node.expression) * max(case_paths, 1)

    def _for_loop_npath(self, node: ASTNode) -> int:
        body_npath = self._node_npath(node.body)
        if hasattr(node.control, 'condition') and node.control.condition:
            condition_npath = max(1, self._node_npath(node.control.condition))
        else:
            condition_npath = 1
        return body_npath + condition_npath

    def _binary_expression_npath(self, node: ASTNode) -> int:
        operator = node.operator
        if operator not in {'&&', '||'}:
            return 1
        left_npath = self._node_npath(node.operandl)
        right_npath = self._node_npath(node.operandr)
        return left_npath + right_npath
