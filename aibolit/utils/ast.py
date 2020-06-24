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
from cached_property import cached_property  # type: ignore
from itertools import islice
from collections import namedtuple

import javalang.tree
from javalang.tree import Node
from typing import Union, Any, Set, Dict, Type, List, Iterator
from networkx import DiGraph, dfs_labeled_edges, dfs_preorder_nodes  # type: ignore


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
    VARIABLE_DECLARATION = auto()
    VARIABLE_DECLARATOR = auto()
    VOID_CLASS_REFERENCE = auto()
    WHILE_STATEMENT = auto()


MethodInvocationParams = namedtuple('MethodInvocationParams', ['object_name', 'method_name'])


class AST:
    _NODE_SKIPED = -1

    def __init__(self, javalang_ast_root: Node):
        self.tree = DiGraph()
        self.root = self._build_networkx_tree_from_javalang(javalang_ast_root)

    def __str__(self) -> str:
        printed_graph = ''
        depth = 0
        print_step = 4
        for _, destination, edge_type in dfs_labeled_edges(self.tree, self.root):
            if edge_type == 'forward':
                if depth > 0:
                    printed_graph += ' ' * depth + '|---'
                printed_graph += str(self.tree.nodes[destination]['type']) + '\n'
                depth += print_step
            elif edge_type == 'reverse':
                depth -= print_step
        return printed_graph

    def subtrees_with_root_type(self, root_type: ASTNodeType) -> Iterator[List[int]]:
        '''
        Yields subtrees with given type of the root.
        If such subtrees are one including the other, only the larger one is
        going to be in resulted sequence.
        '''
        is_inside_subtree = False
        current_subtree_root = -1  # all node indexes are positive
        subtree: List[int] = []
        for _, destination, edge_type in dfs_labeled_edges(self.tree, self.root):
            if edge_type == 'forward':
                if is_inside_subtree:
                    subtree.append(destination)
                elif self.tree.nodes[destination]['type'] == root_type:
                    subtree.append(destination)
                    is_inside_subtree = True
                    current_subtree_root = destination
            elif edge_type == 'reverse' and destination == current_subtree_root:
                is_inside_subtree = False
                yield subtree
                subtree = []

    def children_with_type(self, node: int, child_type: ASTNodeType) -> Iterator[int]:
        '''
        Yields children of node with given type.
        '''
        for child in self.tree.succ[node]:
            if self.tree.nodes[child]['type'] == child_type:
                yield child

    @cached_property
    def node_types(self) -> List[ASTNodeType]:
        '''
        Yields types of nodes in preorder tree traversal.
        '''
        return [self.tree.nodes[node]['type'] for node in dfs_preorder_nodes(self.tree, self.root)]

    def nodes_by_type(self, type: ASTNodeType) -> Iterator[int]:
        return (node for node in self.tree.nodes if self.tree.nodes[node]['type'] == type)

    def get_attr(self, node: int, attr_name: str, default_value: Any = None) -> Any:
        return self.tree.nodes[node].get(attr_name, default_value)

    def get_type(self, node: int) -> ASTNodeType:
        return self.get_attr(node, 'type')

    def get_method_invoked_name(self, invocation_node: int) -> MethodInvocationParams:
        assert(self.get_type(invocation_node) == ASTNodeType.METHOD_INVOCATION)
        # first two STRING nodes represent object and method names
        object_name, method_name = islice(self.children_with_type(invocation_node, ASTNodeType.STRING), 2)
        return MethodInvocationParams(self.get_attr(object_name, 'string'),
                                      self.get_attr(method_name, 'string'))

    def _build_networkx_tree_from_javalang(self, javalang_node: Node) -> int:
        node_index = len(self.tree) + 1
        self.tree.add_node(node_index)
        self._extract_javalang_node_attributes(javalang_node, node_index)

        for children_item in javalang_node.children:
            if type(children_item) == list:
                for child in children_item:
                    child_node_index = self._handle_javalang_ast_node(child)
                    if child_node_index != AST._NODE_SKIPED:
                        self.tree.add_edge(node_index, child_node_index)
            else:
                child_node_index = self._handle_javalang_ast_node(children_item)
                if child_node_index != AST._NODE_SKIPED:
                    self.tree.add_edge(node_index, child_node_index)

        return node_index

    def _extract_javalang_node_attributes(self, javalang_node: Node, node_index: int) -> None:
        self.tree.add_node(node_index, type=AST._javalang_types_map[type(javalang_node)])

        if hasattr(javalang_node.position, 'line'):
            self.tree.add_node(node_index, source_code_line=javalang_node.position.line)

    def _handle_javalang_ast_node(self, javalang_node: Union[Node, Set[Any], str]) -> int:
        if isinstance(javalang_node, Node):
            return self._build_networkx_tree_from_javalang(javalang_node)
        elif isinstance(javalang_node, set):
            return self._handle_javalang_collection_node(javalang_node)
        elif isinstance(javalang_node, str):
            return self._handle_javalang_string_node(javalang_node)

        return AST._NODE_SKIPED

    def _handle_javalang_string_node(self, string_node: str) -> int:
        node_index = len(self.tree) + 1
        self.tree.add_node(node_index, type=ASTNodeType.STRING, string=string_node)
        return node_index

    def _handle_javalang_collection_node(self, collection_node: Set[Any]) -> int:
        node_index = len(self.tree) + 1
        self.tree.add_node(node_index, type=ASTNodeType.COLLECTION)
        for item in collection_node:
            if type(item) == str:
                string_node_index = self._handle_javalang_string_node(item)
                self.tree.add_edge(node_index, string_node_index)
            elif item is not None:
                raise RuntimeError('Unexpected javalang AST node type {} inside \
                                    "COLLECTION" node'.format(type(item)))
        return node_index

    _javalang_types_map: Dict[Type, ASTNodeType] = {
        javalang.tree.Annotation: ASTNodeType.ANNOTATION,
        javalang.tree.AnnotationDeclaration: ASTNodeType.ANNOTATION_DECLARATION,
        javalang.tree.AnnotationMethod: ASTNodeType.ANNOTATION_METHOD,
        javalang.tree.ArrayCreator: ASTNodeType.ARRAY_CREATOR,
        javalang.tree.ArrayInitializer: ASTNodeType.ARRAY_INITIALIZER,
        javalang.tree.ArraySelector: ASTNodeType.ARRAY_SELECTOR,
        javalang.tree.AssertStatement: ASTNodeType.ASSERT_STATEMENT,
        javalang.tree.Assignment: ASTNodeType.ASSIGNMENT,
        javalang.tree.BasicType: ASTNodeType.BASIC_TYPE,
        javalang.tree.BinaryOperation: ASTNodeType.BINARY_OPERATION,
        javalang.tree.BlockStatement: ASTNodeType.BLOCK_STATEMENT,
        javalang.tree.BreakStatement: ASTNodeType.BREAK_STATEMENT,
        javalang.tree.Cast: ASTNodeType.CAST,
        javalang.tree.CatchClause: ASTNodeType.CATCH_CLAUSE,
        javalang.tree.CatchClauseParameter: ASTNodeType.CATCH_CLAUSE_PARAMETER,
        javalang.tree.ClassCreator: ASTNodeType.CLASS_CREATOR,
        javalang.tree.ClassDeclaration: ASTNodeType.CLASS_DECLARATION,
        javalang.tree.ClassReference: ASTNodeType.CLASS_REFERENCE,
        javalang.tree.CompilationUnit: ASTNodeType.COMPILATION_UNIT,
        javalang.tree.ConstantDeclaration: ASTNodeType.CONSTANT_DECLARATION,
        javalang.tree.ConstructorDeclaration: ASTNodeType.CONSTRUCTOR_DECLARATION,
        javalang.tree.ContinueStatement: ASTNodeType.CONTINUE_STATEMENT,
        javalang.tree.Creator: ASTNodeType.CREATOR,
        javalang.tree.Declaration: ASTNodeType.DECLARATION,
        javalang.tree.Documented: ASTNodeType.DOCUMENTED,
        javalang.tree.DoStatement: ASTNodeType.DO_STATEMENT,
        javalang.tree.ElementArrayValue: ASTNodeType.ELEMENT_ARRAY_VALUE,
        javalang.tree.ElementValuePair: ASTNodeType.ELEMENT_VALUE_PAIR,
        javalang.tree.EnhancedForControl: ASTNodeType.ENHANCED_FOR_CONTROL,
        javalang.tree.EnumBody: ASTNodeType.ENUM_BODY,
        javalang.tree.EnumConstantDeclaration: ASTNodeType.ENUM_CONSTANT_DECLARATION,
        javalang.tree.EnumDeclaration: ASTNodeType.ENUM_DECLARATION,
        javalang.tree.ExplicitConstructorInvocation: ASTNodeType.EXPLICIT_CONSTRUCTOR_INVOCATION,
        javalang.tree.Expression: ASTNodeType.EXPRESSION,
        javalang.tree.FieldDeclaration: ASTNodeType.FIELD_DECLARATION,
        javalang.tree.ForControl: ASTNodeType.FOR_CONTROL,
        javalang.tree.FormalParameter: ASTNodeType.FORMAL_PARAMETER,
        javalang.tree.ForStatement: ASTNodeType.FOR_STATEMENT,
        javalang.tree.IfStatement: ASTNodeType.IF_STATEMENT,
        javalang.tree.Import: ASTNodeType.IMPORT,
        javalang.tree.InferredFormalParameter: ASTNodeType.INFERRED_FORMAL_PARAMETER,
        javalang.tree.InnerClassCreator: ASTNodeType.INNER_CLASS_CREATOR,
        javalang.tree.InterfaceDeclaration: ASTNodeType.INTERFACE_DECLARATION,
        javalang.tree.Invocation: ASTNodeType.INVOCATION,
        javalang.tree.LambdaExpression: ASTNodeType.LAMBDA_EXPRESSION,
        javalang.tree.Literal: ASTNodeType.LITERAL,
        javalang.tree.LocalVariableDeclaration: ASTNodeType.LOCAL_VARIABLE_DECLARATION,
        javalang.tree.Member: ASTNodeType.MEMBER,
        javalang.tree.MemberReference: ASTNodeType.MEMBER_REFERENCE,
        javalang.tree.MethodDeclaration: ASTNodeType.METHOD_DECLARATION,
        javalang.tree.MethodInvocation: ASTNodeType.METHOD_INVOCATION,
        javalang.tree.MethodReference: ASTNodeType.METHOD_REFERENCE,
        javalang.tree.PackageDeclaration: ASTNodeType.PACKAGE_DECLARATION,
        javalang.tree.Primary: ASTNodeType.PRIMARY,
        javalang.tree.ReferenceType: ASTNodeType.REFERENCE_TYPE,
        javalang.tree.ReturnStatement: ASTNodeType.RETURN_STATEMENT,
        javalang.tree.Statement: ASTNodeType.STATEMENT,
        javalang.tree.StatementExpression: ASTNodeType.STATEMENT_EXPRESSION,
        javalang.tree.SuperConstructorInvocation: ASTNodeType.SUPER_CONSTRUCTOR_INVOCATION,
        javalang.tree.SuperMemberReference: ASTNodeType.SUPER_MEMBER_REFERENCE,
        javalang.tree.SuperMethodInvocation: ASTNodeType.SUPER_METHOD_INVOCATION,
        javalang.tree.SwitchStatement: ASTNodeType.SWITCH_STATEMENT,
        javalang.tree.SwitchStatementCase: ASTNodeType.SWITCH_STATEMENT_CASE,
        javalang.tree.SynchronizedStatement: ASTNodeType.SYNCHRONIZED_STATEMENT,
        javalang.tree.TernaryExpression: ASTNodeType.TERNARY_EXPRESSION,
        javalang.tree.This: ASTNodeType.THIS,
        javalang.tree.ThrowStatement: ASTNodeType.THROW_STATEMENT,
        javalang.tree.TryResource: ASTNodeType.TRY_RESOURCE,
        javalang.tree.TryStatement: ASTNodeType.TRY_STATEMENT,
        javalang.tree.Type: ASTNodeType.TYPE,
        javalang.tree.TypeArgument: ASTNodeType.TYPE_ARGUMENT,
        javalang.tree.TypeDeclaration: ASTNodeType.TYPE_DECLARATION,
        javalang.tree.TypeParameter: ASTNodeType.TYPE_PARAMETER,
        javalang.tree.VariableDeclaration: ASTNodeType.VARIABLE_DECLARATION,
        javalang.tree.VariableDeclarator: ASTNodeType.VARIABLE_DECLARATOR,
        javalang.tree.VoidClassReference: ASTNodeType.VOID_CLASS_REFERENCE,
        javalang.tree.WhileStatement: ASTNodeType.WHILE_STATEMENT,
    }
