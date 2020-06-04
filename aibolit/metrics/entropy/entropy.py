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

import javalang
from typing import List
import numpy as np  # type: ignore
from scipy.stats import entropy  # type: ignore

from aibolit.utils.encoding_detector import read_text_with_autodetected_encoding


class Entropy:
    def __init__(self):
        pass

    def __file_to_tokens(self, filename: str) -> List[str]:
        '''Takes path to java class file and returns tokens'''
        source_code = read_text_with_autodetected_encoding(filename)
        tokens = javalang.tokenizer.tokenize(source_code)
        return [token.value for token in tokens]

    def value(self, filename: str):
        tokens = self.__file_to_tokens(filename)
        _, counts = np.unique(tokens, return_counts=True)
        return entropy(counts)
