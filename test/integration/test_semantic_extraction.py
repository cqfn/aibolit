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
