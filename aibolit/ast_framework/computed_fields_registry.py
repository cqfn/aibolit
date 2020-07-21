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

from collections import defaultdict
from typing import Dict, Callable, Any

from aibolit.ast_framework import ASTNode, ASTNodeType


class _ComputedFieldsRegistry:
    def __init__(self) -> None:
        RegistryType = Dict[ASTNodeType, Dict[str, Callable[[ASTNode], Any]]]
        self._registry: RegistryType = defaultdict(dict)

    def register(
        self,
        compute_field: Callable[[ASTNode], Any],
        name: str,
        *node_types: ASTNodeType,
    ) -> None:
        for node_type in node_types:
            computed_fields = self._registry[node_type]
            if name in computed_fields:
                raise RuntimeError(
                    f'Registry already has computed field '
                    f'named "{name}" for node type {node_type}.'
                )

            computed_fields[name] = compute_field

    def get_fields(self, node_type: ASTNodeType) -> Dict[str, Callable[[ASTNode], Any]]:
        return self._registry[node_type]

    def clear(self) -> None:
        self._registry = defaultdict(dict)


computed_fields_registry = _ComputedFieldsRegistry()
