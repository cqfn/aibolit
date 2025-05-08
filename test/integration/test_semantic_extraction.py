# SPDX-FileCopyrightText: Copyright (c) 2020 Aibolit
# SPDX-License-Identifier: MIT

from pathlib import Path
from os import listdir

from tqdm import tqdm

from aibolit.ast_framework import AST, ASTNodeType
from aibolit.utils.ast_builder import build_ast
from aibolit.extract_method_baseline.extract_semantic import extract_method_statements_semantic

samples_path = Path(__file__).absolute().parent / "samples"

if __name__ == "__main__":
    print(f"Processed files in {samples_path}:")
    for filepath in tqdm(listdir(samples_path)):
        ast = AST.build_from_javalang(build_ast(samples_path / filepath))
        for type_declaration in ast.get_root().types:
            if type_declaration.node_type == ASTNodeType.CLASS_DECLARATION:
                for method_declaration in type_declaration.methods:
                    method_ast = ast.get_subtree(method_declaration)
                    try:
                        extract_method_statements_semantic(method_ast)
                    except Exception as e:
                        raise RuntimeError(
                            f"Failed to extract semantic from method {method_declaration.name} "
                            f"in class {type_declaration.name} in file {samples_path / filepath}."
                        ) from e
