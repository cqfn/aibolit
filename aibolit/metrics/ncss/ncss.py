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


from aibolit.utils.ast import AST


class NCSSMetric():
    def __init__(self):
        pass

    def value(self, filename: str):
        if len(filename) == 0:
            raise ValueError('Empty file for analysis')

        tree = AST(filename).value()

        metric = 0
        for path, node in tree:
            node_type = str(type(node))
            if 'Statement' in node_type:
                metric += 1
            elif 'VariableDeclarator' == node_type:
                metric += 1
            elif 'Assignment' == node_type:
                metric += 1
            elif 'Declaration' in node_type and 'LocalVariableDeclaration' not in node_type \
                 and 'PackageDeclaration' not in node_type:
                metric += 1

        return metric
