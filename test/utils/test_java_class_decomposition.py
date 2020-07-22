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

from unittest import TestCase, skip
from pathlib import Path

from aibolit.ast_framework.java_class_decomposition import decompose_java_class
from aibolit.ast_framework.java_package import JavaPackage


@skip("Usage of deprecated API breaks test")
class JavaClassDecompositionTestSuite(TestCase):
    def test_strong_decomposition(self):
        java_package = JavaPackage(Path(__file__).parent.absolute() / 'MethodUseOtherMethodExample.java')
        java_class = java_package.java_classes['MethodUseOtherMethod']
        class_components = decompose_java_class(java_class, 'strong')
        self.assertEqual(len(class_components), 7)

    def test_weak_decomposition(self):
        java_package = JavaPackage(Path(__file__).parent.absolute() / 'MethodUseOtherMethodExample.java')
        java_class = java_package.java_classes['MethodUseOtherMethod']
        class_components = decompose_java_class(java_class, 'weak')
        self.assertEqual(len(class_components), 5)
