from networkx import DiGraph
from typing import Callable, Iterator, Any, TYPE_CHECKING

from veniq.ast_framework import ASTNode
from .constants import NODE, NodeId

if TYPE_CHECKING:
    from .block import Block
    from ._nodes_factory import TraverseCallback  # noqa: F401


class Statement:
    def __init__(
        self,
        graph: DiGraph,
        id: NodeId,
        block_factory: Callable[[DiGraph, NodeId], "Block"],
        traverse_function: Callable[[DiGraph, NodeId, "TraverseCallback", "TraverseCallback"], None],
    ):
        self._graph = graph
        self._id = id
        self._block_factory = block_factory
        self._traverse_function = traverse_function

    @property
    def node(self) -> ASTNode:
        return self._graph.nodes[self._id][NODE]

    @property
    def has_nested_blocks(self) -> bool:
        return self._graph.out_degree(self._id) > 0

    @property
    def nested_blocks(self) -> Iterator["Block"]:
        for block_id in self._graph.successors(self._id):
            yield self._block_factory(self._graph, block_id)

    @property
    def parent_block(self) -> "Block":
        block_id = next(self._graph.predecessors(self._id))
        return self._block_factory(self._graph, block_id)

    def traverse(
        self, on_node_entering: "TraverseCallback", on_node_leaving: "TraverseCallback" = lambda _: None
    ):
        self._traverse_function(self._graph, self._id, on_node_entering, on_node_leaving)

    def __eq__(self, other: Any) -> bool:
        if other is None:
            return False

        if not isinstance(other, Statement):
            raise NotImplementedError(f"Only Statement objects are supported, got {other}")

        return self._graph == other._graph and self._id == other._id
