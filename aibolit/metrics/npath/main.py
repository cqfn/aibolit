# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
# SPDX-License-Identifier: MIT

import math
import os
import shutil
import subprocess
import tempfile
import uuid
from typing import Iterable, TypedDict

from bs4 import BeautifulSoup

from aibolit.ast_framework import AST, ASTNode, ASTNodeType
from aibolit.utils.ast_builder import build_ast


class NPathMethodReport(TypedDict):
    class_name: str
    method_name: str
    complexity: int


class NPathMetric():
    """Main NPath Complexity class."""

    input = ''

    def __init__(self, input):
        self.input = input

    def value(self, showoutput=False):
        """Run NPath Complexity analaysis"""

        if len(self.input) == 0:
            raise ValueError('Empty file for analysis')
        if shutil.which('mvn') is None:
            return self._value_without_maven()
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

    def _value_without_maven(self):
        if not os.path.isfile(self.input):
            raise Exception(' '.join(['File', self.input, 'does not exist']))
        ast = AST.build_from_javalang(build_ast(self.input))
        complexity = MvnFreeNPathMetric(ast).value()
        return {'data': [{'file': self.input, 'complexity': complexity}], 'errors': []}

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
        return sum(method['complexity'] for method in self.report())

    def report(self) -> list[NPathMethodReport]:
        return [
            {
                'class_name': class_declaration.name,
                'method_name': method.name,
                'complexity': self._method_npath(method),
            }
            for class_ast in self.ast.subtrees(ASTNodeType.CLASS_DECLARATION)
            for class_declaration in [class_ast.root()]
            for method in class_declaration.methods
        ]

    def _method_npath(self, method_node: ASTNode) -> int:
        return self._node_npath(method_node.body)

    def _node_npath(self, node: ASTNode) -> int:
        if isinstance(node, list):
            return self._sequence_npath(node)

        def default_handler(node: ASTNode) -> int:
            return self._composite_npath(node)

        dispatcher = {
            ASTNodeType.IF_STATEMENT: self._if_npath,
            ASTNodeType.SWITCH_STATEMENT: self._switch_npath,
            ASTNodeType.FOR_STATEMENT: self._for_loop_npath,
            ASTNodeType.WHILE_STATEMENT: self._while_loop_npath,
            ASTNodeType.EXPRESSION: self._expression_npath,
            ASTNodeType.BINARY_OPERATION: self._expression_npath,
            ASTNodeType.TERNARY_EXPRESSION: self._expression_npath,
        }

        handler = dispatcher.get(node.node_type, default_handler)
        return handler(node)

    def _composite_npath(self, node: ASTNode) -> int:
        return self._sequence_npath(node.children)

    def _sequence_npath(self, nodes: Iterable[ASTNode]) -> int:
        return max(1, math.prod(self._node_npath(child) for child in nodes))

    def _if_npath(self, node: ASTNode) -> int:
        condition_npath = self._expression_npath(node.condition)
        then_npath = self._node_npath(node.then_statement)
        else_npath = (
            self._node_npath(node.else_statement)
            if node.else_statement is not None
            else 1
        )
        return condition_npath + then_npath + else_npath

    def _switch_npath(self, node: ASTNode) -> int:
        npath = self._expression_npath(node.expression)
        has_case = False
        has_default = False
        for case_group in node.cases:
            if len(case_group.case):
                has_case = True
            else:
                has_default = True
            null_statements = max(0, len(case_group.case) - 1)
            npath += self._node_npath(case_group.statements) + null_statements
        return npath + int(not has_case) + int(not has_default)

    def _for_loop_npath(self, node: ASTNode) -> int:
        control_npath = self._expression_npath(node.control)
        body_npath = self._node_npath(node.body)
        return control_npath + body_npath + 1

    def _while_loop_npath(self, node: ASTNode) -> int:
        condition_npath = self._expression_npath(node.condition)
        body_npath = self._node_npath(node.body)
        return condition_npath + body_npath + 1

    def _expression_npath(self, node: ASTNode) -> int:
        def default_handler(node: ASTNode) -> int:
            return self._composite_expression_npath(node)

        dispatcher = {
            ASTNodeType.BINARY_OPERATION: self._binary_expression_npath,
            ASTNodeType.TERNARY_EXPRESSION: self._ternary_npath,
        }
        return dispatcher.get(node.node_type, default_handler)(node)

    def _composite_expression_npath(self, node: ASTNode) -> int:
        return sum(self._expression_npath(child) for child in node.children)

    def _binary_expression_npath(self, node: ASTNode) -> int:
        left_npath = self._expression_npath(node.operandl)
        right_npath = self._expression_npath(node.operandr)
        return left_npath + right_npath + (node.operator in ('&&', '||'))

    def _ternary_npath(self, node: ASTNode) -> int:
        return self._composite_expression_npath(node) + 2
