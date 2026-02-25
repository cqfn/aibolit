# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
# SPDX-License-Identifier: MIT
import dataclasses
from enum import Enum, auto

from typing import List, Set, Optional


class ScopeStatusFlags(Enum):
    ONLY_VARIABLE_DECLARATIONS_PRESENT = auto()
    INSIDE_VARIABLE_DECLARATION_SUBTREE = auto()
    INSIDE_CALLING_SUPER_CLASS_CONSTRUCTOR_SUBTREE = auto()
    INSIDE_ANNOTATION_SUBTREE = auto()


class DefaultScopeStatus:
    def value(self) -> Set[ScopeStatusFlags]:
        return {ScopeStatusFlags.ONLY_VARIABLE_DECLARATIONS_PRESENT}


@dataclasses.dataclass(slots=True)
class ScopeStatus:
    _scope_stack: List[Set[ScopeStatusFlags]] = \
        dataclasses.field(default_factory=lambda: [DefaultScopeStatus().value()])

    def status(self) -> Set[ScopeStatusFlags]:
        try:
            return self._scope_stack[-1]
        except IndexError:
            raise RuntimeError('No scopes registered.')

    def add_flag(self, flag: ScopeStatusFlags) -> None:
        try:
            self._scope_stack[-1].add(flag)
        except IndexError:
            raise RuntimeError('No scopes registered.')

    def remove_flag(self, flag: ScopeStatusFlags) -> None:
        try:
            self._scope_stack[-1].discard(flag)
        except IndexError:
            raise RuntimeError('No scopes registered.')

    def enter_new_scope(
        self, new_scope_status: Optional[Set[ScopeStatusFlags]] = None
    ) -> None:
        if new_scope_status is None:
            new_scope_status = DefaultScopeStatus().value()
        # Copy new_scope_status to prevent its modification
        self._scope_stack.append(new_scope_status.copy())

    def leave_current_scope(self) -> None:
        try:
            self._scope_stack.pop()
        except IndexError:
            raise RuntimeError('No scopes registered.')
