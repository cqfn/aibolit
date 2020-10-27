from typing import Callable, Dict, List, Optional, NamedTuple, Union

from veniq.ast_framework import ASTNode, ASTNodeType
from .constants import BlockReason


class BlockInfo(NamedTuple):
    reason: BlockReason
    statements: List[ASTNode]
    origin_statement: Optional[ASTNode] = None


def extract_blocks_from_statement(statement: ASTNode) -> List[BlockInfo]:
    try:
        return _block_extractors[statement.node_type](statement)
    except KeyError:
        raise NotImplementedError(f"Node {statement.node_type} is not supported.")


def _extract_blocks_from_plain_statement(statement: ASTNode) -> List[BlockInfo]:
    return []


def _extract_blocks_from_single_block_statement_factory(
    field_name: str,
) -> Callable[[ASTNode], List[BlockInfo]]:
    def extract_blocks_from_single_block_statement(statement: ASTNode) -> List[BlockInfo]:
        return [
            BlockInfo(
                reason=BlockReason.SINGLE_BLOCK,
                statements=_unwrap_block_to_statements_list(getattr(statement, field_name)),
            )
        ]

    return extract_blocks_from_single_block_statement


def _extract_blocks_from_if_branching(statement: ASTNode) -> List[BlockInfo]:
    block_infos: List[BlockInfo] = []

    while statement is not None and statement.node_type == ASTNodeType.IF_STATEMENT:
        block_infos.append(
            BlockInfo(
                reason=BlockReason.THEN_BRANCH,
                statements=_unwrap_block_to_statements_list(statement.then_statement),
                origin_statement=statement
            )
        )

        statement = statement.else_statement

    if statement is not None:
        block_infos.append(
            BlockInfo(
                reason=BlockReason.ELSE_BRANCH,
                statements=_unwrap_block_to_statements_list(statement)
            )
        )

    return block_infos


def _extract_blocks_from_switch_branching(statement: ASTNode) -> List[BlockInfo]:
    return [BlockInfo(
        reason=BlockReason.SINGLE_BLOCK,
        statements=[
            switch_statement
            for switch_case in statement.cases
            for switch_statement in switch_case.statements
        ]
    )]


def _extract_blocks_from_try_statement(statement: ASTNode) -> List[BlockInfo]:
    block_infos: List[BlockInfo] = []

    if statement.resources is not None:
        block_infos.append(
            BlockInfo(
                reason=BlockReason.TRY_RESOURCES,
                statements=statement.resources
            )
        )

    block_infos.append(
        BlockInfo(
            reason=BlockReason.TRY_BLOCK,
            statements=_unwrap_block_to_statements_list(statement.block)
        )
    )

    if statement.catches is not None:
        for catch_clause in statement.catches:
            block_infos.append(
                BlockInfo(
                    reason=BlockReason.CATCH_BLOCK,
                    statements=_unwrap_block_to_statements_list(catch_clause.block)
                )
            )

    if statement.finally_block is not None:
        block_infos.append(
            BlockInfo(
                reason=BlockReason.FINALLY_BLOCK,
                statements=_unwrap_block_to_statements_list(statement.finally_block)
            )
        )

    return block_infos


def _unwrap_block_to_statements_list(
    block_statement_or_statement_list: Union[ASTNode, List[ASTNode]]
) -> List[ASTNode]:
    if isinstance(block_statement_or_statement_list, ASTNode):
        if block_statement_or_statement_list.node_type == ASTNodeType.BLOCK_STATEMENT:
            return block_statement_or_statement_list.statements
        else:
            return [block_statement_or_statement_list]

    return block_statement_or_statement_list


_block_extractors: Dict[ASTNodeType, Callable[[ASTNode], List[BlockInfo]]] = {
    # plain statements
    ASTNodeType.ASSERT_STATEMENT: _extract_blocks_from_plain_statement,
    ASTNodeType.BREAK_STATEMENT: _extract_blocks_from_plain_statement,
    ASTNodeType.CONTINUE_STATEMENT: _extract_blocks_from_plain_statement,
    ASTNodeType.RETURN_STATEMENT: _extract_blocks_from_plain_statement,
    ASTNodeType.STATEMENT_EXPRESSION: _extract_blocks_from_plain_statement,
    ASTNodeType.THROW_STATEMENT: _extract_blocks_from_plain_statement,
    ASTNodeType.LOCAL_VARIABLE_DECLARATION: _extract_blocks_from_plain_statement,
    ASTNodeType.TRY_RESOURCE: _extract_blocks_from_plain_statement,
    # single block statements
    ASTNodeType.BLOCK_STATEMENT: _extract_blocks_from_single_block_statement_factory("statements"),
    ASTNodeType.DO_STATEMENT: _extract_blocks_from_single_block_statement_factory("body"),
    ASTNodeType.FOR_STATEMENT: _extract_blocks_from_single_block_statement_factory("body"),
    ASTNodeType.METHOD_DECLARATION: _extract_blocks_from_single_block_statement_factory("body"),
    ASTNodeType.SYNCHRONIZED_STATEMENT: _extract_blocks_from_single_block_statement_factory("block"),
    ASTNodeType.WHILE_STATEMENT: _extract_blocks_from_single_block_statement_factory("body"),
    ASTNodeType.SWITCH_STATEMENT: _extract_blocks_from_switch_branching,
    # multi block statements
    ASTNodeType.IF_STATEMENT: _extract_blocks_from_if_branching,
    ASTNodeType.TRY_STATEMENT: _extract_blocks_from_try_statement,
}
