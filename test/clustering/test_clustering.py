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


# flake8: noqa
from unittest import TestCase
from collections import OrderedDict
from aibolit.clustering.clustering import process_statement


class ClusteringTestCase(TestCase):
      example = OrderedDict([
             (2, []),
             (3, ['manifests', 'rcs', 'length']), 
             (4, ['rcs', 'length', 'i']),
             (5, ['rec']),
             (6, ['rcs', 'i']),
             (7, ['rcs', 'i', 'rec', 'grabRes']),
             # (8, ['rcs', 'i']),
             (8, []),
             (9, ['rcs', 'i', 'rec', 'grabNonFileSetRes']),
             (10, []),
             (11, ['length', 'rec', 'j']),
             (12, ['rec', 'j', 'name', 'getName', 'replace']),
             (13, ['rcs', 'i']),
             (14, ['rcs', 'i', 'afs']),
             (15, ['rcs', 'afs', 'equals', 'getFullpath', 'getProj']),
             (16, ['name', 'afs', 'getFullpath', 'getProj']),
             (17, ['afs', 'equals', 'getProj', 'getPref']),
             (18, ['afs', 'getProj', 'getPref', 'pr']),
             (19, ['pr', 'endsWith']),
             (20,['pr']),
             (21,[]),
             (22,['name', 'pr']),
             (23,[]),
             (24,[]),
             (25,['name', 'equalsIgnoreCase']),
             (26, ['manifests', 'rec', 'j', 'i']),
             (27,[]),
             (28,[]),
             (29,[]),
             (30, ['manifests', 'i']),
             (31, ['manifests', 'i']),
             (32,[]),
             (33,[]),
             (34, ['manifests']),
            ]
           )

      def test_article(self):
            statements = list(self.example.keys())

            self.assertEqual(process_statement(self.example, statements, 1), 
            [[3, 12], [13, 22], [30, 31]], 'Error on STEP 1')
            
            self.assertEqual(process_statement(self.example, statements, 2), 
            [[3, 12], [13, 25], [30, 34]], 'Error on STEP 2')

            self.assertEqual(process_statement(self.example, statements, 3), 
            [[3, 25], [26, 34]], 'Error on STEP 3')

            self.assertEqual(process_statement(self.example, statements, 4), 
            [[3, 25], [26, 34]], 'Error on STEP 4')

            self.assertEqual(process_statement(self.example, statements, 5), 
            [[3, 25], [26, 34]], 'Error on STEP 5')
            
            self.assertEqual(process_statement(self.example, statements, 11), 
            [[3, 34]], 'Error on STEP 11')

            self.assertEqual(process_statement(self.example, statements, 12), 
            [[3, 34]], 'Error on STEP 12')
