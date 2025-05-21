# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

import networkx as nx  # type: ignore
from aibolit.utils.ast_builder import build_ast

from aibolit.utils.cohesiongraph import CohesionGraph


class LCOM4:

    coh = CohesionGraph()

    def __init__(self):
        pass

    def value(self, filename: str):

        tree = build_ast(filename)
        G = self.coh.value(tree)
        return nx.number_connected_components(G)
