from typing import Tuple, Union

FldExh = Tuple[str, Tuple[str, str]]
MthExh = Tuple[str, Tuple[Tuple[str, str], ...]]
EdgeNode = Union[MthExh, FldExh]


class GraphBuilder:

    @staticmethod
    def add_vertices_edges(G, edge_type: str, first_node: EdgeNode, second_node: EdgeNode) -> None:
        """Adds nodes to graph G

        Gets two objects as input and
        adds nodes and an edge between.
        If nodes already exist:
        creates an edge between
        """

        G.add_node(first_node[0] + str(hash(first_node[1])))
        G.add_node((second_node[0]) + str(hash(second_node[1])))
        G.add_edge(first_node[0] + str(hash(first_node[1])),
                   (second_node[0]) + str(hash(second_node[1])), type=edge_type)
