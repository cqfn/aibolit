# SPDX-FileCopyrightText: Copyright (c) 2020 Aibolit
# SPDX-License-Identifier: MIT

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
