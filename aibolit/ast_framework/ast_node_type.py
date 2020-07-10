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

from typing import Dict, Type, List

from javalang import tree


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


javalang_types_map: Dict[Type, ASTNodeType] = {
    tree.Annotation: ASTNodeType.ANNOTATION,
    tree.AnnotationDeclaration: ASTNodeType.ANNOTATION_DECLARATION,
    tree.AnnotationMethod: ASTNodeType.ANNOTATION_METHOD,
    tree.ArrayCreator: ASTNodeType.ARRAY_CREATOR,
    tree.ArrayInitializer: ASTNodeType.ARRAY_INITIALIZER,
    tree.ArraySelector: ASTNodeType.ARRAY_SELECTOR,
    tree.AssertStatement: ASTNodeType.ASSERT_STATEMENT,
    tree.Assignment: ASTNodeType.ASSIGNMENT,
    tree.BasicType: ASTNodeType.BASIC_TYPE,
    tree.BinaryOperation: ASTNodeType.BINARY_OPERATION,
    tree.BlockStatement: ASTNodeType.BLOCK_STATEMENT,
    tree.BreakStatement: ASTNodeType.BREAK_STATEMENT,
    tree.Cast: ASTNodeType.CAST,
    tree.CatchClause: ASTNodeType.CATCH_CLAUSE,
    tree.CatchClauseParameter: ASTNodeType.CATCH_CLAUSE_PARAMETER,
    tree.ClassCreator: ASTNodeType.CLASS_CREATOR,
    tree.ClassDeclaration: ASTNodeType.CLASS_DECLARATION,
    tree.ClassReference: ASTNodeType.CLASS_REFERENCE,
    tree.CompilationUnit: ASTNodeType.COMPILATION_UNIT,
    tree.ConstantDeclaration: ASTNodeType.CONSTANT_DECLARATION,
    tree.ConstructorDeclaration: ASTNodeType.CONSTRUCTOR_DECLARATION,
    tree.ContinueStatement: ASTNodeType.CONTINUE_STATEMENT,
    tree.Creator: ASTNodeType.CREATOR,
    tree.Declaration: ASTNodeType.DECLARATION,
    tree.Documented: ASTNodeType.DOCUMENTED,
    tree.DoStatement: ASTNodeType.DO_STATEMENT,
    tree.ElementArrayValue: ASTNodeType.ELEMENT_ARRAY_VALUE,
    tree.ElementValuePair: ASTNodeType.ELEMENT_VALUE_PAIR,
    tree.EnhancedForControl: ASTNodeType.ENHANCED_FOR_CONTROL,
    tree.EnumBody: ASTNodeType.ENUM_BODY,
    tree.EnumConstantDeclaration: ASTNodeType.ENUM_CONSTANT_DECLARATION,
    tree.EnumDeclaration: ASTNodeType.ENUM_DECLARATION,
    tree.ExplicitConstructorInvocation: ASTNodeType.EXPLICIT_CONSTRUCTOR_INVOCATION,
    tree.Expression: ASTNodeType.EXPRESSION,
    tree.FieldDeclaration: ASTNodeType.FIELD_DECLARATION,
    tree.ForControl: ASTNodeType.FOR_CONTROL,
    tree.FormalParameter: ASTNodeType.FORMAL_PARAMETER,
    tree.ForStatement: ASTNodeType.FOR_STATEMENT,
    tree.IfStatement: ASTNodeType.IF_STATEMENT,
    tree.Import: ASTNodeType.IMPORT,
    tree.InferredFormalParameter: ASTNodeType.INFERRED_FORMAL_PARAMETER,
    tree.InnerClassCreator: ASTNodeType.INNER_CLASS_CREATOR,
    tree.InterfaceDeclaration: ASTNodeType.INTERFACE_DECLARATION,
    tree.Invocation: ASTNodeType.INVOCATION,
    tree.LambdaExpression: ASTNodeType.LAMBDA_EXPRESSION,
    tree.Literal: ASTNodeType.LITERAL,
    tree.LocalVariableDeclaration: ASTNodeType.LOCAL_VARIABLE_DECLARATION,
    tree.Member: ASTNodeType.MEMBER,
    tree.MemberReference: ASTNodeType.MEMBER_REFERENCE,
    tree.MethodDeclaration: ASTNodeType.METHOD_DECLARATION,
    tree.MethodInvocation: ASTNodeType.METHOD_INVOCATION,
    tree.MethodReference: ASTNodeType.METHOD_REFERENCE,
    tree.PackageDeclaration: ASTNodeType.PACKAGE_DECLARATION,
    tree.Primary: ASTNodeType.PRIMARY,
    tree.ReferenceType: ASTNodeType.REFERENCE_TYPE,
    tree.ReturnStatement: ASTNodeType.RETURN_STATEMENT,
    tree.Statement: ASTNodeType.STATEMENT,
    tree.StatementExpression: ASTNodeType.STATEMENT_EXPRESSION,
    tree.SuperConstructorInvocation: ASTNodeType.SUPER_CONSTRUCTOR_INVOCATION,
    tree.SuperMemberReference: ASTNodeType.SUPER_MEMBER_REFERENCE,
    tree.SuperMethodInvocation: ASTNodeType.SUPER_METHOD_INVOCATION,
    tree.SwitchStatement: ASTNodeType.SWITCH_STATEMENT,
    tree.SwitchStatementCase: ASTNodeType.SWITCH_STATEMENT_CASE,
    tree.SynchronizedStatement: ASTNodeType.SYNCHRONIZED_STATEMENT,
    tree.TernaryExpression: ASTNodeType.TERNARY_EXPRESSION,
    tree.This: ASTNodeType.THIS,
    tree.ThrowStatement: ASTNodeType.THROW_STATEMENT,
    tree.TryResource: ASTNodeType.TRY_RESOURCE,
    tree.TryStatement: ASTNodeType.TRY_STATEMENT,
    tree.Type: ASTNodeType.TYPE,
    tree.TypeArgument: ASTNodeType.TYPE_ARGUMENT,
    tree.TypeDeclaration: ASTNodeType.TYPE_DECLARATION,
    tree.TypeParameter: ASTNodeType.TYPE_PARAMETER,
    tree.VariableDeclaration: ASTNodeType.VARIABLE_DECLARATION,
    tree.VariableDeclarator: ASTNodeType.VARIABLE_DECLARATOR,
    tree.VoidClassReference: ASTNodeType.VOID_CLASS_REFERENCE,
    tree.WhileStatement: ASTNodeType.WHILE_STATEMENT,
}

node_attributes_by_type: Dict[ASTNodeType, List[str]] = {
    ASTNodeType.ANNOTATION_DECLARATION: [
        "annotations",
        "body",
        "documentation",
        "modifiers",
        "name",
    ],
    ASTNodeType.ANNOTATION_METHOD: [
        "annotations",
        "default",
        "dimensions",
        "modifiers",
        "name",
        "return_type",
    ],
    ASTNodeType.ANNOTATION: ["element", "name"],
    ASTNodeType.ARRAY_CREATOR: [
        "dimensions",
        "initializer",
        "postfix_operators",
        "prefix_operators",
        "qualifier",
        "selectors",
        "type",
    ],
    ASTNodeType.ARRAY_INITIALIZER: ["initializers"],
    ASTNodeType.ARRAY_SELECTOR: ["index"],
    ASTNodeType.ASSERT_STATEMENT: ["condition", "label", "value"],
    ASTNodeType.ASSIGNMENT: ["expressionl", "type", "value"],
    ASTNodeType.BASIC_TYPE: ["dimensions", "name"],
    ASTNodeType.BINARY_OPERATION: ["operandl", "operandr", "operator"],
    ASTNodeType.BLOCK_STATEMENT: ["label", "statements"],
    ASTNodeType.BREAK_STATEMENT: ["goto", "label"],
    ASTNodeType.CAST: ["expression", "type"],
    ASTNodeType.CATCH_CLAUSE_PARAMETER: ["annotations", "name", "modifiers", "types"],
    ASTNodeType.CATCH_CLAUSE: ["block", "label", "parameter"],
    ASTNodeType.CLASS_CREATOR: [
        "arguments",
        "body",
        "constructor_type_arguments",
        "postfix_operators",
        "prefix_operators",
        "qualifier",
        "selectors",
        "type",
    ],
    ASTNodeType.CLASS_DECLARATION: [
        "annotations",
        "body",
        "documentation",
        "extends",
        "implements",
        "modifiers",
        "name",
        "type_parameters",
    ],
    ASTNodeType.CLASS_REFERENCE: [
        "postfix_operators",
        "prefix_operators",
        "qualifier",
        "selectors",
        "type",
    ],
    ASTNodeType.COMPILATION_UNIT: ["imports", "package", "types"],
    ASTNodeType.CONSTANT_DECLARATION: [
        "annotations",
        "declarators",
        "documentation",
        "modifiers",
        "type",
    ],
    ASTNodeType.CONSTRUCTOR_DECLARATION: [
        "annotations",
        "body",
        "documentation",
        "modifiers",
        "name",
        "parameters",
        "throws",
        "type_parameters",
    ],
    ASTNodeType.CONTINUE_STATEMENT: ["goto", "label"],
    ASTNodeType.CREATOR: [
        "postfix_operators",
        "prefix_operators",
        "qualifier",
        "selectors",
        "type",
    ],
    ASTNodeType.DECLARATION: ["annotations", "modifiers"],
    ASTNodeType.DO_STATEMENT: ["body", "condition", "label"],
    ASTNodeType.DOCUMENTED: ["documentation"],
    ASTNodeType.ELEMENT_ARRAY_VALUE: ["values"],
    ASTNodeType.ELEMENT_VALUE_PAIR: ["name", "value"],
    ASTNodeType.ENHANCED_FOR_CONTROL: ["iterable", "var"],
    ASTNodeType.ENUM_BODY: ["constants", "declarations"],
    ASTNodeType.ENUM_CONSTANT_DECLARATION: [
        "annotations",
        "arguments",
        "body",
        "documentation",
        "modifiers",
        "name",
    ],
    ASTNodeType.ENUM_DECLARATION: [
        "annotations",
        "body",
        "documentation",
        "implements",
        "modifiers",
        "name",
    ],
    ASTNodeType.EXPLICIT_CONSTRUCTOR_INVOCATION: [
        "arguments",
        "postfix_operators",
        "prefix_operators",
        "qualifier",
        "selectors",
        "type_arguments",
    ],
    ASTNodeType.EXPRESSION: [],
    ASTNodeType.FIELD_DECLARATION: [
        "annotations",
        "declarators",
        "documentation",
        "modifiers",
        "type",
    ],
    ASTNodeType.FOR_CONTROL: ["condition", "init", "update"],
    ASTNodeType.FOR_STATEMENT: ["body", "control", "label"],
    ASTNodeType.FORMAL_PARAMETER: [
        "annotations",
        "modifiers",
        "name",
        "type",
        "varargs",
    ],
    ASTNodeType.IF_STATEMENT: [
        "condition",
        "else_statement",
        "label",
        "then_statement",
    ],
    ASTNodeType.IMPORT: ["path", "static", "wildcard"],
    ASTNodeType.INFERRED_FORMAL_PARAMETER: ["name"],
    ASTNodeType.INNER_CLASS_CREATOR: [
        "arguments",
        "body",
        "constructor_type_arguments",
        "postfix_operators",
        "prefix_operators",
        "qualifier",
        "selectors",
        "type",
    ],
    ASTNodeType.INTERFACE_DECLARATION: [
        "annotations",
        "body",
        "documentation",
        "extends",
        "modifiers",
        "name",
        "type_parameters",
    ],
    ASTNodeType.INVOCATION: [
        "arguments",
        "postfix_operators",
        "prefix_operators",
        "qualifier",
        "selectors",
        "type_arguments",
    ],
    ASTNodeType.LAMBDA_EXPRESSION: ["body", "parameters"],
    ASTNodeType.LITERAL: [
        "postfix_operators",
        "prefix_operators",
        "qualifier",
        "selectors",
        "value",
    ],
    ASTNodeType.LOCAL_VARIABLE_DECLARATION: [
        "annotations",
        "declarators",
        "modifiers",
        "type",
    ],
    ASTNodeType.MEMBER_REFERENCE: [
        "member",
        "postfix_operators",
        "prefix_operators",
        "qualifier",
        "selectors",
    ],
    ASTNodeType.MEMBER: ["documentation"],
    ASTNodeType.METHOD_DECLARATION: [
        "annotations",
        "body",
        "documentation",
        "modifiers",
        "name",
        "parameters",
        "return_type",
        "throws",
        "type_parameters",
    ],
    ASTNodeType.METHOD_INVOCATION: [
        "arguments",
        "member",
        "postfix_operators",
        "prefix_operators",
        "qualifier",
        "selectors",
        "type_arguments",
    ],
    ASTNodeType.METHOD_REFERENCE: ["expression", "method", "type_arguments"],
    ASTNodeType.PACKAGE_DECLARATION: [
        "annotations",
        "documentation",
        "modifiers",
        "name",
    ],
    ASTNodeType.PRIMARY: [
        "postfix_operators",
        "prefix_operators",
        "qualifier",
        "selectors",
    ],
    ASTNodeType.REFERENCE_TYPE: ["arguments", "dimensions", "name", "sub_type"],
    ASTNodeType.RETURN_STATEMENT: ["expression", "label"],
    ASTNodeType.STATEMENT_EXPRESSION: ["expression", "label"],
    ASTNodeType.STATEMENT: ["label"],
    ASTNodeType.SUPER_CONSTRUCTOR_INVOCATION: [
        "arguments",
        "postfix_operators",
        "prefix_operators",
        "qualifier",
        "selectors",
        "type_arguments",
    ],
    ASTNodeType.SUPER_MEMBER_REFERENCE: [
        "member",
        "postfix_operators",
        "prefix_operators",
        "qualifier",
        "selectors",
    ],
    ASTNodeType.SUPER_METHOD_INVOCATION: [
        "arguments",
        "member",
        "postfix_operators",
        "prefix_operators",
        "qualifier",
        "selectors",
        "type_arguments",
    ],
    ASTNodeType.SWITCH_STATEMENT_CASE: ["case", "statements"],
    ASTNodeType.SWITCH_STATEMENT: ["cases", "expression", "label"],
    ASTNodeType.SYNCHRONIZED_STATEMENT: ["block", "label", "lock"],
    ASTNodeType.TERNARY_EXPRESSION: ["condition", "if_false", "if_true"],
    ASTNodeType.THIS: [
        "postfix_operators",
        "prefix_operators",
        "qualifier",
        "selectors",
    ],
    ASTNodeType.THROW_STATEMENT: ["expression", "label"],
    ASTNodeType.TRY_RESOURCE: ["annotations", "name", "modifiers", "type", "value"],
    ASTNodeType.TRY_STATEMENT: [
        "block",
        "catches",
        "finally_block",
        "label",
        "resources",
    ],
    ASTNodeType.TYPE_ARGUMENT: ["pattern_type", "type"],
    ASTNodeType.TYPE_DECLARATION: [
        "annotations",
        "body",
        "documentation",
        "modifiers",
        "name",
    ],
    ASTNodeType.TYPE_PARAMETER: ["extends", "name"],
    ASTNodeType.TYPE: ["dimensions", "name"],
    ASTNodeType.VARIABLE_DECLARATION: [
        "annotations",
        "declarators",
        "modifiers",
        "type",
    ],
    ASTNodeType.VARIABLE_DECLARATOR: ["dimensions", "initializer", "name"],
    ASTNodeType.VOID_CLASS_REFERENCE: [
        "postfix_operators",
        "prefix_operators",
        "qualifier",
        "selectors",
        "type",
    ],
    ASTNodeType.WHILE_STATEMENT: ["body", "condition", "label"],
}
