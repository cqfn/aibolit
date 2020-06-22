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

from enum import Enum, auto

from typing import List, Set


class ScopeStatusFlags(Enum):
    ONLY_VARIABLE_DECLARATIONS_PRESENT = auto()
    INSIDE_VARIABLE_DECLARATION_SUBTREE = auto()
    INSIDE_CALLING_SUPER_CLASS_CONSTRUCTOR_SUBTREE = auto()
    INSIDE_ANNOTATION_SUBTREE = auto()


class ScopeStatus:
    _default_scope_status: Set[ScopeStatusFlags] = \
        {ScopeStatusFlags.ONLY_VARIABLE_DECLARATIONS_PRESENT}

    def __init__(self):
        # Copy _default_scope_status to prevent its modification
        self._scope_stack: List[Set[ScopeStatusFlags]] = \
            [ScopeStatus._default_scope_status.copy()]

    def get_status(self):
        try:
            return self._scope_stack[-1]
        except IndexError:
            raise RuntimeError("No scopes registered.")

    def add_flag(self, flag):
        try:
            self._scope_stack[-1].add(flag)
        except IndexError:
            raise RuntimeError("No scopes registered.")

    def remove_flag(self, flag):
        try:
            self._scope_stack[-1].discard(flag)
        except IndexError:
            raise RuntimeError("No scopes registered.")

    def enter_new_scope(self, new_scope_status=_default_scope_status):
        # Copy new_scope_status to prevent its modification
        self._scope_stack.append(new_scope_status.copy())

    def leave_current_scope(self):
        try:
            self._scope_stack.pop()
        except IndexError:
            raise RuntimeError("No scopes registered.")
