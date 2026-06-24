# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
# SPDX-License-Identifier: MIT


class RemoveComments:

    def __init__(self):
        pass

    @staticmethod
    def _trim_comment_only_indent(result):
        while result and result[-1] not in '\n\r':
            if result[-1] not in ' \t':
                return
            result.pop()

    @staticmethod
    def _consume_comment(symbol, next_symbol, result, state):
        if state['mode'] == 'line_comment':
            if symbol == '\n':
                result.append(symbol)
                state['mode'] = None
            return 1
        if state['mode'] == 'block_comment':
            if symbol == '*' and next_symbol == '/':
                state['mode'] = None
                return 2
            if symbol == '\n':
                result.append(symbol)
            return 1
        return 0

    @staticmethod
    def _consume_literal(symbol, state):
        if state['mode'] not in {'string', 'char'}:
            return False
        if state['escaped']:
            state['escaped'] = False
        elif symbol == '\\':
            state['escaped'] = True
        elif symbol == '"' and state['mode'] == 'string':
            state['mode'] = None
        elif symbol == "'" and state['mode'] == 'char':
            state['mode'] = None
        return True

    @staticmethod
    def _enter_literal(symbol, state):
        if symbol == '"':
            state['mode'] = 'string'
            state['escaped'] = False
            return True
        if symbol == "'":
            state['mode'] = 'char'
            state['escaped'] = False
            return True
        return False

    @staticmethod
    def _enter_comment(symbol, next_symbol, result, state):
        if symbol != '/' or next_symbol not in {'/', '*'}:
            return 0
        result.pop()
        RemoveComments._trim_comment_only_indent(result)
        state['mode'] = 'line_comment' if next_symbol == '/' else 'block_comment'
        return 2

    @staticmethod
    def remove_comments(string):
        result = []
        state = {'mode': None, 'escaped': False}
        index = 0
        while index < len(string):
            symbol = string[index]
            next_symbol = string[index + 1] if index + 1 < len(string) else ''

            step = RemoveComments._consume_comment(symbol, next_symbol, result, state)
            if step:
                index += step
                continue

            result.append(symbol)

            if RemoveComments._consume_literal(symbol, state):
                index += 1
                continue

            if RemoveComments._enter_literal(symbol, state):
                index += 1
                continue

            step = RemoveComments._enter_comment(symbol, next_symbol, result, state)
            if step:
                index += step
                continue

            index += 1

        return ''.join(result)
