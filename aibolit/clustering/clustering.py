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


from collections import Counter
from typing import Iterator, Tuple, List # flake8 --ignore=F401
from collections import OrderedDict
from argparse import ArgumentParser
from aibolit.utils.ast_builder import build_ast
from aibolit.extract_method_baseline.extract_semantic import extract_method_statements_semantic
from aibolit.ast_framework import ASTNode, AST, ASTNodeType


def check_is_common(dict_file, statement_1: ASTNode, statement_2: ASTNode) -> bool:
    joined_names: Counter = Counter(dict_file[statement_1] + dict_file[statement_2])
    duplicates = {element: count for element, count in joined_names.items() if count > 1}.keys()
    return len(list(duplicates)) >= 1


def is_in_range(elem: int, values: List[int]) -> bool:
    return elem >= values[0] and elem <= values[1]


def process_statement(dict_file: OrderedDict, list_statements: List[int], step: int) -> List[List[int]]:
    clusters: List[List[int]] = []
    for stat_1 in list_statements:
        for stat_2 in list_statements[:stat_1.line + step]:
            if stat_1.line < stat_2.line and check_is_common(dict_file, stat_1, stat_2):
                if len(clusters) != 0 and is_in_range(stat_1.line, clusters[-1]):
                    if not is_in_range(stat_2.line, clusters[-1]):
                        clusters[-1][1] = stat_2.line
                else:
                    clusters.append([stat_1.line, stat_2.line])
    return clusters


def SEMI_beta(dict_file: OrderedDict, method_len: int) -> dict:
    algo_step = {}
    statements = list(dict_file.keys())
    for step in range(1, method_len + 1):
        clusters = process_statement(dict_file, statements, step)
        algo_step[step] = clusters
    return algo_step


def _reprocess_dict(method_semantic: OrderedDict) -> OrderedDict:
    reprocessed_dict = OrderedDict([])
    for statement in method_semantic.keys():
        new_values = []
        new_values += list(method_semantic[statement].used_variables)
        new_values += list(method_semantic[statement].used_objects)
        new_values += list(method_semantic[statement].used_methods)
        reprocessed_dict.update({statement: new_values})
    return reprocessed_dict


def _get_clusters(methods_ast_and_class_name: Iterator[Tuple[AST, str]]) -> List:
    for method_ast, class_name in methods_ast_and_class_name:
        method_clusters = []
        method_name = method_ast.get_root().name
        method_semantic = extract_method_statements_semantic(method_ast)
        reporcessed_dict = _reprocess_dict(method_semantic)
        method_length = list(reporcessed_dict.keys())[-1].line
        print('-' * 50)
        print('Starting algorithm for method: ', method_name)
        print('-' * 50)
        clusters = SEMI_beta(reporcessed_dict, method_length)
        method_clusters.append((method_name, clusters))
    return method_clusters


if __name__ == '__main__':
    parser = ArgumentParser(description="Extracts semantic from specified methods")
    parser.add_argument("-f", "--file", required=True,
                        help="File path to JAVA source code for extracting semantic")
    parser.add_argument("-c", "--class", default=None, dest="class_name",
                        help="Class name of method to parse, if omitted all classes are considered")
    parser.add_argument("-m", "--method", default=None, dest="method_name",
                        help="Method name to parse, if omitted all method are considered")
    parser.add_argument("-v", "--verbose", default=None, dest="verbose_mode",
                        help="Mode to print clusters for each step")

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

    method_with_clusters = _get_clusters(methods_ast_and_class_name)
    print(method_with_clusters)
