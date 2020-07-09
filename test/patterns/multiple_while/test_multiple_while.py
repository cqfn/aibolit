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

from unittest import TestCase
from aibolit.patterns.multiple_while.multiple_while import MultipleWhile
from pathlib import Path


class TestMultipleWhile(TestCase):

    def test_simple(self):
        lines = MultipleWhile().value(Path(__file__).parent.absolute() / 'Simple.java')
        self.assertEqual(lines, [2])

    def test_one_while(self):
        lines = MultipleWhile().value(Path(__file__).parent.absolute() / 'OneWhile.java')
        self.assertEqual(lines, [])

    def test_if_while(self):
        lines = MultipleWhile().value(Path(__file__).parent.absolute() / 'IfWhile.java')
        self.assertEqual(lines, [2])

    def test_multiple_while(self):
        lines = MultipleWhile().value(Path(__file__).parent.absolute() / 'MultipleWhile.java')
        self.assertEqual(lines, [])
