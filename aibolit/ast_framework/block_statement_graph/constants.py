from enum import Enum

NodeId = int

# networkx field names
NODE = "node"
BLOCK_REASON = "block_reason"
ORIGIN_STATEMENT = "origin_statement"


class NodeType(Enum):
    Statement = "Statement"
    Block = "Block"


class BlockReason(Enum):
    SINGLE_BLOCK = "SINGLE_BLOCK"
    THEN_BRANCH = "THEN_BRANCH"
    ELSE_BRANCH = "ELSE_BRANCH"
    TRY_RESOURCES = "TRY_RESOURCES"
    TRY_BLOCK = "TRY_BLOCK"
    CATCH_BLOCK = "CATCH_BLOCK"
    FINALLY_BLOCK = "FINALLY_BLOCK"
