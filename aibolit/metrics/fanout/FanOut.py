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

from typing import Set

from aibolit.ast_framework import AST, ASTNode, ASTNodeType


class FanOut:
    """
    Fan Out metric is defined as the number of other classes referenced by a class.
    """

    def value(self, ast: AST) -> int:
        fan_out = 0
        for class_declaration in ast.get_subtrees(ASTNodeType.CLASS_DECLARATION):
            fan_out += self._calculate_class_fan_out(class_declaration)

        return fan_out

    def _calculate_class_fan_out(self, java_class: AST) -> int:
        class_declaration = java_class.get_root()
        assert class_declaration.node_type == ASTNodeType.CLASS_DECLARATION

        used_classes_names: Set[str] = set()

        for type_reference in java_class.get_proxy_nodes(ASTNodeType.REFERENCE_TYPE):
            used_class_name = self._get_class_name_from_type_reference(type_reference)
            if used_class_name not in FanOut._excluded_class_names:
                used_classes_names.add(used_class_name)

        # remove name of the class
        used_classes_names -= {class_declaration.name}
        return len(used_classes_names)

    def _get_class_name_from_type_reference(self, type_reference: ASTNode) -> str:
        assert type_reference.node_type == ASTNodeType.REFERENCE_TYPE

        # type_reference 'name' field may not have a name of class in case this class
        # is referenced from packages, like 'package1.package2.class'.
        # To get class name we need to iterate over subtypes first and in the end get class name.
        while isinstance(type_reference.sub_type, ASTNode):
            type_reference = type_reference.sub_type

        return type_reference.name

    # exception are used from https://checkstyle.sourceforge.io/config_metrics.html#ClassFanOutComplexity
    # basic types ('int', 'long', etc.) are not used, because ASTNodeType.REFERENCE_TYPE match only class types
    _excluded_class_names = {
        "ArrayIndexOutOfBoundsException",
        "ArrayList",
        "Boolean",
        "Byte",
        "Character",
        "Class",
        "Deprecated",
        "Deque",
        "Double",
        "Exception",
        "Float",
        "FunctionalInterface",
        "HashMap",
        "HashSet",
        "IllegalArgumentException",
        "IllegalStateException",
        "IndexOutOfBoundsException",
        "Integer",
        "LinkedList",
        "List",
        "Long",
        "Map",
        "NullPointerException",
        "Object",
        "Override",
        "Queue",
        "RuntimeException",
        "SafeVarargs",
        "SecurityException",
        "Set",
        "Short",
        "SortedMap",
        "SortedSet",
        "String",
        "StringBuffer",
        "StringBuilder",
        "SuppressWarnings",
        "Throwable",
        "TreeMap",
        "TreeSet",
        "UnsupportedOperationException",
        "Void",
        "System.out",
    }
