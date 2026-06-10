# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
# SPDX-License-Identifier: MIT


class RemoveComments:

    def __init__(self):
        pass

    @staticmethod
    def remove_comments(string):
        result = []
        index = 0
        in_string = False
        in_char = False
        in_line_comment = False
        in_block_comment = False
        escaped = False

        def trim_comment_only_indent():
            while result and result[-1] not in '\n\r':
                if result[-1] not in ' \t':
                    return
                result.pop()

        while index < len(string):
            symbol = string[index]
            next_symbol = string[index + 1] if index + 1 < len(string) else ''

            if in_line_comment:
                if symbol == '\n':
                    result.append(symbol)
                    in_line_comment = False
                index += 1
                continue

            if in_block_comment:
                if symbol == '*' and next_symbol == '/':
                    in_block_comment = False
                    index += 2
                    continue
                if symbol == '\n':
                    result.append(symbol)
                index += 1
                continue

            result.append(symbol)

            if in_string:
                if escaped:
                    escaped = False
                elif symbol == '\\':
                    escaped = True
                elif symbol == '"':
                    in_string = False
                index += 1
                continue

            if in_char:
                if escaped:
                    escaped = False
                elif symbol == '\\':
                    escaped = True
                elif symbol == "'":
                    in_char = False
                index += 1
                continue

            if symbol == '"':
                in_string = True
                index += 1
                continue

            if symbol == "'":
                in_char = True
                index += 1
                continue

            if symbol == '/' and next_symbol == '/':
                result.pop()
                trim_comment_only_indent()
                in_line_comment = True
                index += 2
                continue

            if symbol == '/' and next_symbol == '*':
                result.pop()
                trim_comment_only_indent()
                in_block_comment = True
                index += 2
                continue

            index += 1

        return ''.join(result)
