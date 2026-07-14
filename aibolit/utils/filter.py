# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
# SPDX-License-Identifier: MIT
from typing import List, Tuple, Any, Union, TypeVar, Type
from javalang.tree import (
    AssertStatement,
    Assignment,
    ClassDeclaration,
    FieldDeclaration,
    InterfaceDeclaration,
    LocalVariableDeclaration,
    MemberReference,
    MethodDeclaration,
    MethodInvocation,
    Node,
    ReturnStatement,
    This,
)

FldExh = Tuple[str, Tuple[str, str]]
MthExh = Tuple[str, Tuple[Tuple[str, str], ...]]
HasMember = Union[MemberReference, MethodInvocation]
HasSelector = Union[MemberReference, MethodInvocation, This]
T = TypeVar('T', bound=Node)
S = TypeVar('S', HasSelector, HasMember)
MthNodes = Tuple[tuple, MethodDeclaration]
Nodes = Tuple[tuple, T]
AnyField = Union[FieldDeclaration, LocalVariableDeclaration]


class Filters:

    def __init__(self):
        pass

    def filter_node_lvl(self, node: Node, javalang_class: Type[Node]) -> List[Nodes]:
        """Filters nodes by desired javalang class.

        Gets node(node) of any javalang.Tree type and filters it by
        desired type(javalang_class).
        Returns a generator with (path, node) inside.
        """
        temp_list = []
        for filtered_path, filtered_node in node.filter(javalang_class):
            if self.get_class_depth(filtered_path) == 1:
                temp_list.append((filtered_path, filtered_node))
        return temp_list

    @staticmethod
    def filter_getters_setters(method_node_list: List[MthNodes]) -> List[MthNodes]:
        """Filter actual getter and setter methods.

        Methods whose names merely start with ``get`` or ``set`` remain
        in the returned list unless their bodies match accessor behavior.
        """
        return [
            (path, node)
            for path, node in method_node_list
            if not Filters._is_getter(node) and not Filters._is_setter(node)
        ]

    @staticmethod
    def _is_getter(method_node: MethodDeclaration) -> bool:
        """Check whether a method is a getter."""
        if not method_node.name.startswith('get'):  # type: ignore[unresolved-attribute]
            return False
        body = [
            statement
            for statement in (method_node.body or [])  # type: ignore[unresolved-attribute]
            if not isinstance(statement, AssertStatement)
        ]
        if len(body) != 1 or not isinstance(body[0], ReturnStatement):
            return False
        expression = getattr(body[0], 'expression', None)
        direct_member = isinstance(expression, MemberReference)
        this_member = (
            isinstance(expression, This) and
            len(expression.selectors or []) == 1 and
            isinstance(expression.selectors[0], MemberReference)
        )
        return direct_member or this_member

    @staticmethod
    def _is_setter(method_node: MethodDeclaration) -> bool:
        """Check whether a method is a setter."""
        if (
            not method_node.name.startswith('set') or  # type: ignore[unresolved-attribute]
            method_node.return_type is not None or  # type: ignore[unresolved-attribute]
            not method_node.parameters  # type: ignore[unresolved-attribute]
        ):
            return False
        parameter = method_node.parameters[0].name  # type: ignore[unresolved-attribute]
        for _, assignment in method_node.filter(Assignment):
            value = assignment.value
            if isinstance(value, MemberReference) and value.member == parameter:
                return True
        return False

    @staticmethod
    def get_class_depth(path: tuple) -> int:
        """Returns an int displaying level of given node's nesting level.

        Gets a node of any javalang.tree type and calculates it's nesting level
        Returns an int.
        """

        class_level = 0
        for step in path:
            if isinstance(step, (ClassDeclaration, InterfaceDeclaration, MethodDeclaration)):
                class_level += 1
        return class_level

    @staticmethod
    def exhaust_method(method_node: MethodDeclaration) -> MthExh:
        """ Exhausts name and input vars, types for given MethodDeclaration node.

        Returns a tuple containing name and all parameters
        that given method gets as an input.
        """

        parameter_list = []
        name: str = method_node.name  # type: ignore[unresolved-attribute]
        for parameter in method_node.parameters:  # type: ignore[unresolved-attribute]
            parameter_list.append((parameter.name, parameter.type.name))
        parameter_tuple: Tuple[Tuple[str, str], ...] = tuple(parameter_list)
        return name, parameter_tuple

    @staticmethod
    def exhaust_field(field_node: AnyField) -> FldExh:
        """ Exhausts name and type for given FieldDeclaration or LocalVariableDeclaration node.

        Returns a tuple containing name and type of field.
        """

        # To-Fix: get rid of'type' in parameter_tuple
        name = field_node.declarators[0].name
        try:
            parameter_tuple: Tuple[str, str] = ('type', field_node.type.name)
        except AttributeError:
            return '', ('', '')
        return name, parameter_tuple

    @staticmethod
    def get_arguments(invocation_node: MethodInvocation) -> Tuple[List[str], List[str]]:
        """Gets arguments passed to given MethodInvocation node.

        Returns two tuples containing all arguments and methods passed
        to given MethodInvocation node.
        """

        list_of_funcs = []
        list_of_fields = []
        for argument in invocation_node.arguments:  # type: ignore
            if isinstance(argument, MethodInvocation):
                list_of_funcs.append(argument.member)
            elif isinstance(argument, MemberReference):
                list_of_fields.append(argument.member)
        return list_of_funcs, list_of_fields

    @staticmethod
    def clean_for_repetitions(list_of_exhaust: List[Any]) -> List[Any]:
        """Gets any list and removes all repetitions.

        Returns list with no repetitive objects.
        """

        list_of_exhaust = list(dict.fromkeys(list_of_exhaust))
        return list_of_exhaust
