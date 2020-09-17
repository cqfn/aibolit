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


from collections import OrderedDict
from typing import NamedTuple, Set, Dict, Iterator, Tuple, List
from aibolit.ast_framework import AST, ASTNode, ASTNodeType


class StatementSemantic(NamedTuple):
    used_variables: Set[str] = set()
    used_objects: Set[str] = set()
    used_methods: Set[str] = set()


def extract_method_statements_semantic(method_ast: AST) -> Dict[ASTNode, StatementSemantic]:
    statement_semantic: Dict[ASTNode, StatementSemantic] = OrderedDict()
    for statement in method_ast.get_root().body:
        statement_semantic.update(_extract_statement_semantic(statement, method_ast))

    return statement_semantic


def _extract_statement_semantic(statement: ASTNode, method_ast: AST) -> Dict[ASTNode, StatementSemantic]:
    if statement.node_type == ASTNodeType.BLOCK_STATEMENT:
        return _extract_block_semantic(statement, method_ast)
    elif statement.node_type == ASTNodeType.FOR_STATEMENT:
        return _extract_for_cycle_semantic(statement, method_ast)
    elif statement.node_type in {ASTNodeType.DO_STATEMENT, ASTNodeType.WHILE_STATEMENT}:
        return _extract_while_cycle_semantic(statement, method_ast)
    elif statement.node_type == ASTNodeType.IF_STATEMENT:
        return _extract_if_branching_sematic(statement, method_ast)
    elif statement.node_type == ASTNodeType.SYNCHRONIZED_STATEMENT:
        return _extract_synchronized_block_semantic(statement, method_ast)
    elif statement.node_type == ASTNodeType.SWITCH_STATEMENT:
        return _extract_switch_branching_semantic(statement, method_ast)
    elif statement.node_type == ASTNodeType.TRY_STATEMENT:
        return _extract_try_block_semantic(statement, method_ast)
    elif statement.node_type in {
        ASTNodeType.ASSERT_STATEMENT,
        ASTNodeType.RETURN_STATEMENT,
        ASTNodeType.STATEMENT_EXPRESSION,
        ASTNodeType.THROW_STATEMENT,
        ASTNodeType.LOCAL_VARIABLE_DECLARATION,
    }:
        return _extract_plain_statement_semantic(statement, method_ast)
    elif statement.node_type in {
        ASTNodeType.BREAK_STATEMENT,  # Single keyword statement has no semantic
        ASTNodeType.CONTINUE_STATEMENT,  # Single keyword statement has no semantic
        ASTNodeType.CLASS_DECLARATION,  # Inner class declarations are currently not supported
    }:
        return OrderedDict()

    raise NotImplementedError(f"Extracting semantic from {statement.node_type} is not supported")


def _extract_for_cycle_semantic(statement: ASTNode, method_ast: AST) -> Dict[ASTNode, StatementSemantic]:
    control_subtree = method_ast.get_subtree(statement.control)
    statements_semantic: Dict[ASTNode, StatementSemantic] = OrderedDict(
        [(statement, _extract_semantic_from_ast(control_subtree))]
    )

    statements_semantic.update(_extract_statement_semantic(statement.body, method_ast))

    return statements_semantic


def _extract_block_semantic(statement: ASTNode, method_ast: AST) -> Dict[ASTNode, StatementSemantic]:
    statements_semantic: Dict[ASTNode, StatementSemantic] = OrderedDict()
    for node in statement.statements:
        statements_semantic.update(_extract_statement_semantic(node, method_ast))

    return statements_semantic


def _extract_while_cycle_semantic(statement: ASTNode, method_ast: AST) -> Dict[ASTNode, StatementSemantic]:
    condition_subtree = method_ast.get_subtree(statement.condition)
    statements_semantic: Dict[ASTNode, StatementSemantic] = OrderedDict(
        [(statement, _extract_semantic_from_ast(condition_subtree))]
    )

    statements_semantic.update(_extract_statement_semantic(statement.body, method_ast))

    return statements_semantic


def _extract_if_branching_sematic(statement: ASTNode, method_ast: AST) -> Dict[ASTNode, StatementSemantic]:
    condition_subtree = method_ast.get_subtree(statement.condition)
    statements_semantic: Dict[ASTNode, StatementSemantic] = OrderedDict(
        [(statement, _extract_semantic_from_ast(condition_subtree))]
    )

    statements_semantic.update(_extract_statement_semantic(statement.then_statement, method_ast))

    if statement.else_statement is not None:
        statements_semantic.update(_extract_statement_semantic(statement.else_statement, method_ast))

    return statements_semantic


def _extract_synchronized_block_semantic(
    statement: ASTNode, method_ast: AST
) -> Dict[ASTNode, StatementSemantic]:
    lock_subtree = method_ast.get_subtree(statement.lock)
    statements_semantic: Dict[ASTNode, StatementSemantic] = OrderedDict(
        [(statement, _extract_semantic_from_ast(lock_subtree))]
    )

    for inner_statement in statement.block:
        statements_semantic.update(_extract_statement_semantic(inner_statement, method_ast))
    return statements_semantic


def _extract_switch_branching_semantic(
    statement: ASTNode, method_ast: AST
) -> Dict[ASTNode, StatementSemantic]:
    expression_subtree = method_ast.get_subtree(statement.expression)
    statements_semantic: Dict[ASTNode, StatementSemantic] = OrderedDict(
        [(statement, _extract_semantic_from_ast(expression_subtree))]
    )

    for case in statement.cases:
        for inner_statement in case.statements:
            statements_semantic.update(_extract_statement_semantic(inner_statement, method_ast))

    return statements_semantic


def _extract_try_block_semantic(statement: ASTNode, method_ast: AST) -> Dict[ASTNode, StatementSemantic]:
    statements_semantic: Dict[ASTNode, StatementSemantic] = OrderedDict()

    for resource in statement.resources or []:
        resource_ast = method_ast.get_subtree(resource)
        statements_semantic[resource] = _extract_semantic_from_ast(resource_ast)

    for node in statement.block:
        statements_semantic.update(_extract_statement_semantic(node, method_ast))

    for catch_clause in statement.catches or []:
        for inner_statement in catch_clause.block:
            statements_semantic.update(_extract_statement_semantic(inner_statement, method_ast))

    for node in statement.finally_block or []:
        statements_semantic.update(_extract_statement_semantic(node, method_ast))

    return statements_semantic


def _extract_plain_statement_semantic(statement: ASTNode, method_ast: AST) -> Dict[ASTNode, StatementSemantic]:
    statement_ast = method_ast.get_subtree(statement)
    return OrderedDict([(statement, _extract_semantic_from_ast(statement_ast))])


def _extract_semantic_from_ast(statement_ast: AST) -> StatementSemantic:
    used_variables = set()
    used_objects = set()
    used_methods = set()

    for node in statement_ast.get_proxy_nodes(ASTNodeType.MEMBER_REFERENCE, ASTNodeType.METHOD_INVOCATION):
        if node.node_type == ASTNodeType.MEMBER_REFERENCE:
            used_variables.add(node.member)
        elif node.node_type == ASTNodeType.METHOD_INVOCATION:
            used_methods.add(node.member)

        if node.qualifier is not None:
            used_objects.add(node.qualifier)

    return StatementSemantic(
        used_methods=used_methods, used_objects=used_objects, used_variables=used_variables
    )


def _print_semantic_as_text(methods_ast_and_class_name: Iterator[Tuple[AST, str]]) -> None:
    for method_ast, class_name in methods_ast_and_class_name:
        print(f"{method_ast.get_root().name} method in {class_name} class:")
        method_semantic = extract_method_statements_semantic(method_ast)
        for statement, semantic in method_semantic.items():
            print(f"\t{statement.node_type} on line {statement.line} uses:")

            if len(semantic.used_variables) != 0:
                print("\t\tVariables:")
                for variable_name in semantic.used_variables:
                    print("\t\t\t- " + variable_name)

            if len(semantic.used_objects) != 0:
                print("\t\tObjects:")
                for object_name in semantic.used_objects:
                    print("\t\t\t- " + object_name)

            if len(semantic.used_methods) != 0:
                print("\t\tMethods:")
                for method_name in semantic.used_methods:
                    print("\t\t\t- " + method_name)


if __name__ == "__main__":
    from argparse import ArgumentParser

    from aibolit.utils.ast_builder import build_ast

    parser = ArgumentParser(description="Extracts semantic from specified methods")
    parser.add_argument("-f", "--file", required=True,
                        help="File path to JAVA source code for extracting semantic")
    parser.add_argument("-c", "--class", default=None, dest="class_name",
                        help="Class name of method to parse, if omitted all classes are considered")
    parser.add_argument("-m", "--method", default=None, dest="method_name",
                        help="Method name to parse, if omitted all method are considered")
    args = parser.parse_args()

    ast = AST.build_from_javalang(build_ast(args.file))
    classes_declarations = (
        node for node in ast.get_root().types
        if node.node_type == ASTNodeType.CLASS_DECLARATION
    )

    if args.class_name is not None:
        classes_declarations = (
            node for node in classes_declarations if node.name == args.class_name
        )

    methods_declarations = (
        method_declaration for class_declaration in classes_declarations
        for method_declaration in class_declaration.methods
    )

    if args.method_name is not None:
        methods_declarations = (
            method_declaration for method_declaration in methods_declarations
            if method_declaration.name == args.method_name
        )

    methods_ast_and_class_name = (
        (ast.get_subtree(method_declaration), method_declaration.parent.name)
        for method_declaration in methods_declarations
    )

    _print_semantic_as_text(methods_ast_and_class_name)
