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

from collections import namedtuple
from itertools import islice, repeat, chain

from javalang.tree import Node
from typing import Union, Any, Set, List, Iterator, Tuple, Dict, cast
from networkx import DiGraph, dfs_labeled_edges  # type: ignore

from aibolit.ast_framework.ast_node_type import ASTNodeType
from aibolit.ast_framework._auxiliary_data import javalang_to_ast_node_type, attributes_by_node_type, ASTNodeReference
from aibolit.ast_framework.ast_node import ASTNode

MethodInvocationParams = namedtuple('MethodInvocationParams', ['object_name', 'method_name'])

MemberReferenceParams = namedtuple('MemberReferenceParams', ('object_name', 'member_name', 'unary_operator'))

BinaryOperationParams = namedtuple('BinaryOperationParams', ('operation', 'left_side', 'right_side'))


class AST:
    def __init__(self, networkx_tree: DiGraph, root: int):
        self.tree = networkx_tree
        self.root = root

    @staticmethod
    def build_from_javalang(javalang_ast_root: Node) -> 'AST':
        tree = DiGraph()
        javalang_node_to_index_map: Dict[Node, int] = {}
        root = AST._add_subtree_from_javalang_node(tree, javalang_ast_root,
                                                   javalang_node_to_index_map)
        AST._change_node_attributes_to_index(tree, javalang_node_to_index_map)
        return AST(tree, root)

    def __str__(self) -> str:
        printed_graph = ''
        depth = 0
        print_step = 4
        for _, destination, edge_type in dfs_labeled_edges(self.tree, self.root):
            if edge_type == 'forward':
                if depth > 0:
                    printed_graph += ' ' * depth + '|---'
                node_type = self.get_type(destination)
                printed_graph += str(node_type)
                if node_type == ASTNodeType.STRING:
                    printed_graph += ': ' + self.get_attr(destination, 'string')
                printed_graph += '\n'
                depth += print_step
            elif edge_type == 'reverse':
                depth -= print_step
        return printed_graph

    def get_root(self) -> ASTNode:
        return ASTNode(self.tree, self.root)

    def get_subtrees(self, root_type: ASTNodeType) -> Iterator['AST']:
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
                elif self.tree.nodes[destination]['node_type'] == root_type:
                    subtree.append(destination)
                    is_inside_subtree = True
                    current_subtree_root = destination
            elif edge_type == 'reverse' and destination == current_subtree_root:
                is_inside_subtree = False
                yield AST(self.tree.subgraph(subtree), current_subtree_root)
                subtree = []
                current_subtree_root = -1

    def children_with_type(self, node: int, child_type: ASTNodeType) -> Iterator[int]:
        '''
        Yields children of node with given type.
        '''
        for child in self.tree.succ[node]:
            if self.tree.nodes[child]['node_type'] == child_type:
                yield child

    def list_all_children_with_type(self, node: int, child_type: ASTNodeType) -> List[int]:
        list_node: List[int] = []
        for child in self.tree.succ[node]:
            list_node = list_node + self.list_all_children_with_type(child, child_type)
            if self.tree.nodes[child]['node_type'] == child_type:
                list_node.append(child)
        return sorted(list_node)

    def all_children_with_type(self, node: int, child_type: ASTNodeType) -> Iterator[int]:
        '''
        Yields all children of node with given type.
        '''
        for child in self.list_all_children_with_type(node, child_type):
            yield child

    def get_first_n_children_with_type(self, node: int, child_type: ASTNodeType, quantity: int) -> List[int]:
        '''
        Returns first quantity of children of node with type child_type.
        Resulted list is padded with None to length quantity.
        '''
        children_with_type = (child for child in self.tree.succ[node] if self.get_type(child) == child_type)
        children_with_type_padded = chain(children_with_type, repeat(None))
        return list(islice(children_with_type_padded, 0, quantity))

    def get_binary_operation_name(self, node: int) -> str:
        assert(self.get_type(node) == ASTNodeType.BINARY_OPERATION)
        name_node, = islice(self.children_with_type(node, ASTNodeType.STRING), 1)
        return self.get_attr(name_node, 'string')

    def get_line_number_from_children(self, node: int) -> int:
        for child in self.tree.succ[node]:
            cur_line = self.get_attr(child, 'line')
            if cur_line is not None:
                return cur_line
        return 0

    def get_nodes(self, type: Union[ASTNodeType, None] = None) -> Iterator[int]:
        for node in self.tree.nodes:
            if type is None or self.tree.nodes[node]['node_type'] == type:
                yield node

    def get_attr(self, node: int, attr_name: str, default_value: Any = None) -> Any:
        return self.tree.nodes[node].get(attr_name, default_value)

    def get_type(self, node: int) -> ASTNodeType:
        return self.get_attr(node, 'node_type')

    def get_method_invocation_params(self, invocation_node: int) -> MethodInvocationParams:
        assert(self.get_type(invocation_node) == ASTNodeType.METHOD_INVOCATION)
        # first two STRING nodes represent object and method names
        children = list(self.children_with_type(invocation_node, ASTNodeType.STRING))
        if len(children) == 1:
            return MethodInvocationParams('', self.get_attr(children[0], 'string'))

        return MethodInvocationParams(self.get_attr(children[0], 'string'),
                                      self.get_attr(children[1], 'string'))

    def get_member_reference_params(self, member_reference_node: int) -> MemberReferenceParams:
        assert(self.get_type(member_reference_node) == ASTNodeType.MEMBER_REFERENCE)
        params = [self.get_attr(child, 'string') for child in
                  self.children_with_type(member_reference_node, ASTNodeType.STRING)]

        member_reference_params: MemberReferenceParams
        if len(params) == 1:
            member_reference_params = MemberReferenceParams(object_name='', member_name=params[0],
                                                            unary_operator='')
        elif len(params) == 2:
            member_reference_params = MemberReferenceParams(object_name=params[0], member_name=params[1],
                                                            unary_operator='')
        elif len(params) == 3:
            member_reference_params = MemberReferenceParams(unary_operator=params[0], object_name=params[1],
                                                            member_name=params[2])
        else:
            raise ValueError('Node has 0 or more then 3 children with type "STRING": ' + str(params))

        return member_reference_params

    def get_binary_operation_params(self, binary_operation_node: int) -> BinaryOperationParams:
        assert(self.get_type(binary_operation_node) == ASTNodeType.BINARY_OPERATION)
        operation_node, left_side_node, right_side_node = self.tree.succ[binary_operation_node]
        return BinaryOperationParams(self.get_attr(operation_node, 'string'), left_side_node, right_side_node)

    @staticmethod
    def _add_subtree_from_javalang_node(tree: DiGraph, javalang_node: Union[Node, Set[Any], str],
                                        javalang_node_to_index_map: Dict[Node, int]) -> int:
        node_index, node_type = AST._add_javalang_node(tree, javalang_node)
        if node_index != AST._UNKNOWN_NODE_TYPE and \
           node_type not in {ASTNodeType.COLLECTION, ASTNodeType.STRING}:
            javalang_standard_node = cast(Node, javalang_node)
            javalang_node_to_index_map[javalang_standard_node] = node_index
            AST._add_javalang_children(tree, javalang_standard_node.children, node_index,
                                       javalang_node_to_index_map)
        return node_index

    @staticmethod
    def _add_javalang_children(tree: DiGraph, children: List[Any], parent_index: int,
                               javalang_node_to_index_map: Dict[Node, int]) -> None:
        for child in children:
            if isinstance(child, list):
                AST._add_javalang_children(tree, child, parent_index, javalang_node_to_index_map)
            else:
                child_index = AST._add_subtree_from_javalang_node(tree, child, javalang_node_to_index_map)
                if child_index != AST._UNKNOWN_NODE_TYPE:
                    tree.add_edge(parent_index, child_index)

    @staticmethod
    def _add_javalang_node(tree: DiGraph, javalang_node: Union[Node, Set[Any], str]) -> Tuple[int, ASTNodeType]:
        node_index = AST._UNKNOWN_NODE_TYPE
        node_type = ASTNodeType.UNKNOWN
        if isinstance(javalang_node, Node):
            node_index, node_type = AST._add_javalang_standard_node(tree, javalang_node)
        elif isinstance(javalang_node, set):
            node_index = AST._add_javalang_collection_node(tree, javalang_node)
            node_type = ASTNodeType.COLLECTION
        elif isinstance(javalang_node, str):
            node_index = AST._add_javalang_string_node(tree, javalang_node)
            node_type = ASTNodeType.STRING

        return node_index, node_type

    @staticmethod
    def _add_javalang_standard_node(tree: DiGraph, javalang_node: Node) -> Tuple[int, ASTNodeType]:
        node_index = len(tree) + 1
        node_type = javalang_to_ast_node_type[type(javalang_node)]

        attr_names = attributes_by_node_type[node_type]
        attributes = {attr_name: getattr(javalang_node, attr_name) for attr_name in attr_names}

        attributes['node_type'] = node_type
        attributes['line'] = javalang_node.position.line if javalang_node.position is not None else None

        tree.add_node(node_index, **attributes)
        return node_index, node_type

    @staticmethod
    def _add_javalang_collection_node(tree: DiGraph, collection_node: Set[Any]) -> int:
        node_index = len(tree) + 1
        tree.add_node(node_index, node_type=ASTNodeType.COLLECTION)
        # we expect only strings in collection
        # we add them here as children
        for item in collection_node:
            if type(item) == str:
                string_node_index = AST._add_javalang_string_node(tree, item)
                tree.add_edge(node_index, string_node_index)
            elif item is not None:
                raise ValueError('Unexpected javalang AST node type {} inside \
                                 "COLLECTION" node'.format(type(item)))
        return node_index

    @staticmethod
    def _add_javalang_string_node(tree: DiGraph, string_node: str) -> int:
        node_index = len(tree) + 1
        tree.add_node(node_index, node_type=ASTNodeType.STRING, string=string_node)
        return node_index

    @staticmethod
    def _change_node_attributes_to_index(tree: DiGraph,
                                         javalang_node_to_index_map: Dict[Node, int]) -> None:
        '''
        All javalang fields are stored as is. If some of those fields were pointing to Node
        we change that attribute to have a networkx node index, which represent that node.
        '''
        for node, attributes in tree.nodes.items():
            for attribute_name in attributes:
                attribute_value = attributes[attribute_name]
                if isinstance(attribute_value, Node):
                    node_reference = ASTNodeReference(javalang_node_to_index_map[attribute_value])
                    tree.add_node(node, **{attribute_name: node_reference})
                elif isinstance(attribute_value, list) and \
                        all(isinstance(item, Node) for item in attribute_value):
                    node_references = [ASTNodeReference(javalang_node_to_index_map[item])
                                       for item in attribute_value]
                    tree.add_node(node, **{attribute_name: node_references})

    _UNKNOWN_NODE_TYPE = -1
