# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

from collections import namedtuple
from typing import Union, Any, Callable, Set, List, Iterator, Tuple, Dict, cast, Optional

from javalang.tree import Node
from networkx import DiGraph, dfs_labeled_edges, dfs_preorder_nodes  # type: ignore

from aibolit.ast_framework.ast_node_type import ASTNodeType
from aibolit.ast_framework._auxiliary_data import (
    javalang_to_ast_node_type, attributes_by_node_type, ASTNodeReference
)
from aibolit.ast_framework.ast_node import ASTNode

MethodInvocationParams = namedtuple('MethodInvocationParams', ['object_name', 'method_name'])

MemberReferenceParams = namedtuple(
    'MemberReferenceParams', ('object_name', 'member_name', 'unary_operator')
)

BinaryOperationParams = namedtuple(
    'BinaryOperationParams', ('operation', 'left_side', 'right_side')
)

TraverseCallback = Callable[[ASTNode], None]


class AST:
    def __init__(self, networkx_tree: DiGraph, root: int):
        self._tree = networkx_tree
        self._root = root

    @staticmethod
    def build_from_javalang(javalang_ast_root: Node) -> 'AST':
        tree = DiGraph()
        javalang_node_to_index_map: Dict[Node, int] = {}
        root = AST._add_subtree_from_javalang_node(tree, javalang_ast_root,
                                                   javalang_node_to_index_map)
        AST._replace_javalang_nodes_in_attributes(tree, javalang_node_to_index_map)
        return AST(tree, root)

    def __str__(self) -> str:
        printed_graph = ''
        depth = 0
        for _, destination, edge_type in dfs_labeled_edges(self._tree, self._root):
            if edge_type == 'forward':
                printed_graph += '|   ' * depth
                node_type = self._tree.nodes[destination]['node_type']
                printed_graph += str(node_type) + ': '
                if node_type == ASTNodeType.STRING:
                    printed_graph += self._tree.nodes[destination]['string'] + ', '
                printed_graph += f'node index = {destination}'
                node_line = self._tree.nodes[destination]['line']
                if node_line is not None:
                    printed_graph += f', line = {node_line}'
                printed_graph += '\n'
                depth += 1
            elif edge_type == 'reverse':
                depth -= 1
        return printed_graph

    def root(self) -> ASTNode:
        return ASTNode(self._tree, self._root)

    def __iter__(self) -> Iterator[ASTNode]:
        for node_index in self._tree.nodes:
            yield ASTNode(self._tree, node_index)

    def subtrees(self, *root_type: ASTNodeType) -> Iterator['AST']:
        """
        Yields subtrees with given type of the root.
        If such subtrees are one including the other, only the larger one is
        going to be in resulted sequence.
        """
        is_inside_subtree = False
        current_subtree_root = -1  # all node indexes are positive
        subtree: List[int] = []
        for _, destination, edge_type in dfs_labeled_edges(self._tree, self._root):
            if edge_type == 'forward':
                if is_inside_subtree:
                    subtree.append(destination)
                elif self._tree.nodes[destination]['node_type'] in root_type:
                    subtree.append(destination)
                    is_inside_subtree = True
                    current_subtree_root = destination
            elif edge_type == 'reverse' and destination == current_subtree_root:
                is_inside_subtree = False
                yield AST(self._tree.subgraph(subtree), current_subtree_root)
                subtree = []
                current_subtree_root = -1

    def subtree(self, node: ASTNode) -> 'AST':
        subtree_nodes_indexes = dfs_preorder_nodes(self._tree, node.node_index)
        subtree = self._tree.subgraph(subtree_nodes_indexes)
        return AST(subtree, node.node_index)

    def with_fields_and_methods(
        self,
        allowed_fields_names: Set[str],
        allowed_methods_names: Set[str]
    ) -> 'AST':
        """
        Creates a filtered AST containing only specified fields and methods.

        Args:
            allowed_fields_names: Set of field names to include
            allowed_methods_names: Set of method names to include

        Returns:
            New AST instance with filtered subgraph

        Raises:
            ValueError: If root node is not a CLASS_DECLARATION
        """
        class_declaration = self.root()
        if class_declaration.node_type != ASTNodeType.CLASS_DECLARATION:
            raise ValueError(
                f'Expected {ASTNodeType.CLASS_DECLARATION} node,'
                f' but {class_declaration.node_type} was provided.'
            )
        allowed_nodes = {class_declaration.node_index}

        for field_declaration in class_declaration.fields:
            if allowed_fields_names & set(field_declaration.names):
                field_ast = self.subtree(field_declaration)
                allowed_nodes.update(node.node_index for node in field_ast)

        for method_declaration in class_declaration.methods:
            if method_declaration.name in allowed_methods_names:
                method_ast = self.subtree(method_declaration)
                allowed_nodes.update(node.node_index for node in method_ast)

        return AST(self._tree.subgraph(allowed_nodes), class_declaration.node_index)

    def traverse(
        self,
        on_node_entering: TraverseCallback,
        on_node_leaving: TraverseCallback = lambda node: None,
        source_node: Optional[ASTNode] = None,
        undirected=False
    ):
        traverse_graph = self._tree.to_undirected(as_view=True) if undirected else self._tree
        if source_node is None:
            source_node = self.root()

        for _, destination, edge_type in dfs_labeled_edges(traverse_graph, source_node.node_index):
            if edge_type == 'forward':
                on_node_entering(ASTNode(self._tree, destination))
            elif edge_type == 'reverse':
                on_node_leaving(ASTNode(self._tree, destination))

    def proxy_nodes(self, *types: ASTNodeType) -> Iterator[ASTNode]:
        for node in self._tree.nodes:
            if len(types) == 0 or self._tree.nodes[node]['node_type'] in types:
                yield ASTNode(self._tree, node)

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
                child_index = AST._add_subtree_from_javalang_node(
                    tree, child, javalang_node_to_index_map
                )
                if child_index != AST._UNKNOWN_NODE_TYPE:
                    tree.add_edge(parent_index, child_index)

    @staticmethod
    def _add_javalang_node(
        tree: DiGraph, javalang_node: Union[Node, Set[Any], str]
    ) -> Tuple[int, ASTNodeType]:
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
    def _add_javalang_standard_node(
        tree: DiGraph, javalang_node: Node
    ) -> Tuple[int, ASTNodeType]:
        node_index = len(tree) + 1
        node_type = javalang_to_ast_node_type[type(javalang_node)]

        attr_names = attributes_by_node_type[node_type]
        attributes = {attr_name: getattr(javalang_node, attr_name) for attr_name in attr_names}

        attributes['node_type'] = node_type
        position = getattr(javalang_node, 'position', None)
        attributes['line'] = position.line if position is not None else None

        AST._post_process_javalang_attributes(tree, node_type, attributes)

        tree.add_node(node_index, **attributes)
        return node_index, node_type

    @staticmethod
    def _post_process_javalang_attributes(
        tree: DiGraph, node_type: ASTNodeType, attributes: Dict[str, Any]
    ) -> None:
        """
        Replace some attributes with more appropriate values for convenient work
        """

        if node_type == ASTNodeType.METHOD_DECLARATION and attributes['body'] is None:
            attributes['body'] = []

        if node_type == ASTNodeType.LAMBDA_EXPRESSION and isinstance(attributes['body'], Node):
            attributes['body'] = [attributes['body']]

        if node_type in {ASTNodeType.METHOD_INVOCATION, ASTNodeType.MEMBER_REFERENCE} and \
                attributes['qualifier'] == '':
            attributes['qualifier'] = None

    @staticmethod
    def _add_javalang_collection_node(tree: DiGraph, collection_node: Set[Any]) -> int:
        node_index = len(tree) + 1
        tree.add_node(node_index, node_type=ASTNodeType.COLLECTION, line=None)
        # we expect only strings in collection
        # we add them here as children
        for item in collection_node:
            if isinstance(item, str):
                string_node_index = AST._add_javalang_string_node(tree, item)
                tree.add_edge(node_index, string_node_index)
            elif item is not None:
                raise ValueError(f'Unexpected javalang AST node type {type(item)} inside '
                                 '"COLLECTION" node')
        return node_index

    @staticmethod
    def _add_javalang_string_node(tree: DiGraph, string_node: str) -> int:
        node_index = len(tree) + 1
        tree.add_node(node_index, node_type=ASTNodeType.STRING, string=string_node, line=None)
        return node_index

    @staticmethod
    def _replace_javalang_nodes_in_attributes(tree: DiGraph,
                                              javalang_node_to_index_map: Dict[Node, int]) -> None:
        """
        All javalang nodes found in networkx nodes attributes are replaced
        with references to according networkx nodes.
        Supported attributes types:
         - just javalang Node
         - list of javalang Nodes and other such lists (with any depth)
        """
        for node, attributes in tree.nodes.items():
            for attribute_name in attributes:
                attribute_value = attributes[attribute_name]
                if isinstance(attribute_value, Node):
                    node_reference = AST._create_reference_to_node(attribute_value,
                                                                   javalang_node_to_index_map)
                    tree.nodes[node][attribute_name] = node_reference
                elif isinstance(attribute_value, list):
                    node_references = \
                        AST._replace_javalang_nodes_in_list(attribute_value,
                                                            javalang_node_to_index_map)
                    tree.nodes[node][attribute_name] = node_references

    @staticmethod
    def _replace_javalang_nodes_in_list(javalang_nodes_list: List[Any],
                                        javalang_node_to_index_map: Dict[Node, int]) -> List[Any]:
        """
        javalang_nodes_list: list of javalang Nodes or other such lists (with any depth)
        All javalang nodes are replaces with according references
        NOTICE: Any is used, because mypy does not support recurrent type definitions
        """
        node_references_list: List[Any] = []
        for item in javalang_nodes_list:
            if isinstance(item, Node):
                node_references_list.append(
                    AST._create_reference_to_node(item, javalang_node_to_index_map))
            elif isinstance(item, list):
                node_references_list.append(
                    AST._replace_javalang_nodes_in_list(item, javalang_node_to_index_map))
            elif isinstance(item, (int, str)) or item is None:
                node_references_list.append(item)
            else:
                raise RuntimeError('Cannot parse "Javalang" attribute:\n'
                                   f'{item}\n'
                                   'Expected: Node, list of Nodes, integer or string')

        return node_references_list

    @staticmethod
    def _create_reference_to_node(javalang_node: Node,
                                  javalang_node_to_index_map: Dict[Node, int]) -> ASTNodeReference:
        return ASTNodeReference(javalang_node_to_index_map[javalang_node])

    _UNKNOWN_NODE_TYPE = -1
