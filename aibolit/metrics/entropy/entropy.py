# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

from typing import List, cast

import javalang
import numpy as np
from scipy.stats import entropy

from aibolit.utils.encoding_detector import read_text_with_autodetected_encoding


class Entropy:
    def __init__(self) -> None:
        pass

    def __file_to_tokens(self, filename: str) -> List[str]:
        """Takes path to java class file and returns tokens"""
        source_code = read_text_with_autodetected_encoding(filename)
        tokens = javalang.tokenizer.tokenize(source_code)
        return [token.value for token in tokens]

    def value(self, filename: str) -> float:
        tokens = self.__file_to_tokens(filename)
        _, counts = np.unique(tokens, return_counts=True)
        return cast(float, entropy(counts))
