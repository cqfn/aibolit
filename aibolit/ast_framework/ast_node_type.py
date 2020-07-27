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


class ASTNodeType(Enum):
    ANNOTATION = auto()
    ANNOTATION_DECLARATION = auto()
    ANNOTATION_METHOD = auto()
    ARRAY_CREATOR = auto()
    ARRAY_INITIALIZER = auto()
    ARRAY_SELECTOR = auto()
    ASSERT_STATEMENT = auto()
    ASSIGNMENT = auto()
    BASIC_TYPE = auto()
    BINARY_OPERATION = auto()
    BLOCK_STATEMENT = auto()
    BREAK_STATEMENT = auto()
    CAST = auto()
    CATCH_CLAUSE = auto()
    CATCH_CLAUSE_PARAMETER = auto()
    CLASS_CREATOR = auto()
    CLASS_DECLARATION = auto()
    CLASS_REFERENCE = auto()
    COLLECTION = auto()  # Custom type, represent set (as a node) in AST
    COMPILATION_UNIT = auto()
    CONSTANT_DECLARATION = auto()
    CONSTRUCTOR_DECLARATION = auto()
    CONTINUE_STATEMENT = auto()
    CREATOR = auto()
    DECLARATION = auto()
    DO_STATEMENT = auto()
    DOCUMENTED = auto()
    ELEMENT_ARRAY_VALUE = auto()
    ELEMENT_VALUE_PAIR = auto()
    ENHANCED_FOR_CONTROL = auto()
    ENUM_BODY = auto()
    ENUM_CONSTANT_DECLARATION = auto()
    ENUM_DECLARATION = auto()
    EXPLICIT_CONSTRUCTOR_INVOCATION = auto()
    EXPRESSION = auto()
    FIELD_DECLARATION = auto()
    FOR_CONTROL = auto()
    FOR_STATEMENT = auto()
    FORMAL_PARAMETER = auto()
    IF_STATEMENT = auto()
    IMPORT = auto()
    INFERRED_FORMAL_PARAMETER = auto()
    INNER_CLASS_CREATOR = auto()
    INTERFACE_DECLARATION = auto()
    INVOCATION = auto()
    LAMBDA_EXPRESSION = auto()
    LITERAL = auto()
    LOCAL_VARIABLE_DECLARATION = auto()
    MEMBER = auto()
    MEMBER_REFERENCE = auto()
    METHOD_DECLARATION = auto()
    METHOD_INVOCATION = auto()
    METHOD_REFERENCE = auto()
    PACKAGE_DECLARATION = auto()
    PRIMARY = auto()
    REFERENCE_TYPE = auto()
    RETURN_STATEMENT = auto()
    STATEMENT = auto()
    STATEMENT_EXPRESSION = auto()
    STRING = auto()  # Custom type, represent just string in AST
    SUPER_CONSTRUCTOR_INVOCATION = auto()
    SUPER_MEMBER_REFERENCE = auto()
    SUPER_METHOD_INVOCATION = auto()
    SWITCH_STATEMENT = auto()
    SWITCH_STATEMENT_CASE = auto()
    SYNCHRONIZED_STATEMENT = auto()
    TERNARY_EXPRESSION = auto()
    THIS = auto()
    THROW_STATEMENT = auto()
    TRY_RESOURCE = auto()
    TRY_STATEMENT = auto()
    TYPE = auto()
    TYPE_ARGUMENT = auto()
    TYPE_DECLARATION = auto()
    TYPE_PARAMETER = auto()
    UNKNOWN = auto()  # Custom type, used only in parsing javalang AST
    VARIABLE_DECLARATION = auto()
    VARIABLE_DECLARATOR = auto()
    VOID_CLASS_REFERENCE = auto()
    WHILE_STATEMENT = auto()

    def __str__(self) -> str:
        return self.name.replace('_', ' ').capitalize()
