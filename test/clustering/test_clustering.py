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
# flake8: noqa
from unittest import TestCase

from aibolit.ast_framework import AST
from aibolit.utils.ast_builder import build_ast
from aibolit.extract_method_baseline.extract_semantic import (
    extract_method_statements_semantic,
    StatementSemantic,
)
from aibolit.clustering.clustering import _reprocess_dict, process_statement


class ClusteringTestCase(TestCase):
      current_directory = Path(__file__).absolute().parent

      def article_test(self):
            ast = AST.build_from_javalang(build_ast(self.current_directory / "Article_example.java"))
            class_declaration = ast.get_root().types[0]
            for method_declaration in class_declaration.methods:
                  method_ast = ast.get_subtree(method_declaration)
                  method_name = method_ast.get_root().name
                  method_semantic = extract_method_statements_semantic(method_ast)
                  reporcessed_dict = _reprocess_dict(method_semantic)
                  statements = list(reporcessed_dict.keys())
                  method_length = list(reporcessed_dict.keys())[-1].line

                  self.assertEqual(process_statement(reporcessed_dict, statements, 1), 
                  [[2, 3], [5, 8], [10, 11], [12, 19], [29, 30]], 'Error on STEP 1')
                  
                  self.assertEqual(process_statement(reporcessed_dict, statements, 2), 
                  [[2, 11], [12, 21], [29, 30]], 'Error on STEP 2')

                  self.assertEqual(process_statement(reporcessed_dict, statements, 3), 
                  [[2, 11], [12, 24], [29, 33]], 'Error on STEP 3')

                  self.assertEqual(process_statement(reporcessed_dict, statements, 4), 
                  [[2, 24], [25, 33]], 'Error on STEP 4')

                  self.assertEqual(process_statement(reporcessed_dict, statements, 5), 
                  [[2, 24], [25, 33]], 'Error on STEP 5')
                  
                  self.assertEqual(process_statement(reporcessed_dict, statements, 6), 
                  [[2, 24], [25, 33]], 'Error on STEP 6')

                  self.assertEqual(process_statement(reporcessed_dict, statements, 6), 
                  [[2, 33]], 'Error on STEP 7')
