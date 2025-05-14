# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

import re
from typing import List

from aibolit.utils.encoding_detector import read_text_with_autodetected_encoding


class NullAssignment:
    def value(self, filename: str) -> List:
        source_code = read_text_with_autodetected_encoding(filename)
        pattern = r'[^=!><]=(\s)*null(\s)*;'
        return [lineIndex + 1 for lineIndex, line in
                enumerate(source_code.split('\n')) if re.search(pattern, line)]
