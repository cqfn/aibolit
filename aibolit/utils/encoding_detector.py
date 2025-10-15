# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT
import os

from chardet import detect


def detect_encoding_of_file(filename: str | os.PathLike) -> str:
    with open(filename, 'rb') as target_file:
        return detect_encoding_of_data(target_file.read())


def detect_encoding_of_data(data: bytes) -> str:
    result = detect(data)['encoding']
    return result if result is not None else 'utf-8'


def read_text_with_autodetected_encoding(filename: str | os.PathLike) -> str:
    with open(filename, 'rb') as target_file:
        data = target_file.read()

    if not data:
        return ''  # In case of empty file, return empty string

    encoding = detect_encoding_of_data(data) or 'utf-8'
    return data.decode(encoding)
