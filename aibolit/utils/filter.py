from typing import List, Tuple, Any, Union, TypeVar, Type
from javalang.tree import ClassDeclaration, InterfaceDeclaration, MethodDeclaration, \
    MemberReference, FieldDeclaration, MethodInvocation, This, Node, LocalVariableDeclaration

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
        """Filters nodes by name.

        Gets list of nodes of "MethodDeclaration" type and filters it by
        name, so that no methods with name starting with "set" or "get"
        go to return list.
        Returns a generator with (path, node) inside.
        """

        # ToDo: implement get/set detection with .body
        temp_list = []
        for path, node in method_node_list:
            if node.name.startswith(('get', 'set')):
                pass
            else:
                temp_list.append((path, node))
        return temp_list

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
        name: str = method_node.name
        for parameter in method_node.parameters:
            parameter_list.append((parameter.name, parameter.type.name))
        parameter_tuple: Tuple[Tuple[str, str], ...] = tuple(parameter_list)
        return name, parameter_tuple

    @staticmethod
    def exhaust_field(field_node: AnyField) -> FldExh:
        """ Exhausts name and type for given FieldDeclaration or LocalVariableDeclaration node.

        Returns a tuple containing name and type of field.
        """

        # ToDo: get rid of'type' in parameter_tuple
        name = field_node.declarators[0].name
        try:
            parameter_tuple: Tuple[str, str] = ('type', field_node.type.name)
        except AttributeError:
            return "", ("", "")
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
