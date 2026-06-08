# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
# SPDX-License-Identifier: MIT

from unittest import TestCase
from pathlib import Path
from textwrap import dedent
from typing import Literal

from aibolit.__main__ import flatten
from aibolit.ast_framework import AST, ASTNodeType
from aibolit.ast_framework.java_class_decomposition import decompose_java_class
from aibolit.utils.ast_builder import build_ast, build_ast_from_string


class JavaClassDecompositionTestSuite(TestCase):
    cur_dir = Path(__file__).absolute().parent

    def test_strong_decomposition(self):
        class_ast = self._get_class_ast(
            'MethodUseOtherMethodExample.java', 'MethodUseOtherMethod'
        )
        class_components = decompose_java_class(class_ast, 'strong')
        self.assertEqual(len(class_components), 7)

    def test_weak_decomposition(self):
        class_ast = self._get_class_ast(
            'MethodUseOtherMethodExample.java', 'MethodUseOtherMethod'
        )
        class_components = decompose_java_class(class_ast, 'weak')
        self.assertEqual(len(class_components), 5)

    def _get_class_ast(self, filename: str, class_name: str) -> AST:
        package_ast = AST.build_from_javalang(
            build_ast(Path(__file__).parent.absolute() / filename)
        )
        package_declaration = package_ast.root()
        try:
            class_declaration = next(
                class_declaration
                for class_declaration in package_declaration.types
                if class_declaration.name == class_name
            )
            return package_ast.subtree(class_declaration)

        except StopIteration:
            raise ValueError(
                f"File '{filename}' does not have top level class '{class_name}'."
            )

    def __decompose_with_setter_functionality(self, ignore_getters=False, ignore_setters=False):
        file = str(Path(self.cur_dir, 'LottieImageAsset.java'))
        ast = AST.build_from_javalang(build_ast(file))
        classes_ast = [
            ast.subtree(node)
            for node in ast.root().types
            if node.node_type == ASTNodeType.CLASS_DECLARATION
        ]
        components = list(decompose_java_class(
            classes_ast[0],
            'strong',
            ignore_setters=ignore_setters,
            ignore_getters=ignore_getters))
        function_names = flatten([
            [x.name for x in list(c.proxy_nodes(ASTNodeType.METHOD_DECLARATION))]
            for c in components])
        return function_names

    def test_ignore_setters(self):
        function_names = self.__decompose_with_setter_functionality(ignore_setters=True)
        self.assertTrue('setSomething' not in function_names)
        self.assertTrue('setBitmap' not in function_names)

    def test_do_not_ignore_setters(self):
        function_names = self.__decompose_with_setter_functionality(ignore_setters=False)
        self.assertTrue('setSomething' in function_names)
        self.assertTrue('setBitmap' in function_names)

    def test_ignore_getters(self):
        function_names = self.__decompose_with_setter_functionality(ignore_getters=True)
        self.assertTrue('getWidth' not in function_names)

    def test_do_not_ignore_getters(self):
        function_names = self.__decompose_with_setter_functionality(ignore_getters=False)
        self.assertTrue('getWidth' in function_names)


class TestDecomposeJavaClass:
    def test_empty_class(self) -> None:
        content = dedent(
            '''\
            class Dummy {}
            '''
        ).strip()
        assert _decompose_java_class_from_string(
            content=content,
            strength='strong',
        ) == {
            'num_components': 0,
            'field_names': [],
            'method_names': [],
        }

    def test_class_with_ctor_ignored(self) -> None:
        content = dedent(
            '''\
            class Dummy {
                public Dummy() {};
            }
            '''
        ).strip()
        assert _decompose_java_class_from_string(
            content=content,
            strength='strong',
        ) == {
            'num_components': 0,
            'field_names': [],
            'method_names': [],
        }

    def test_class_with_ctor_and_one_attribute(self) -> None:
        content = dedent(
            '''\
            class Dummy {
                private int value;
                public Dummy(int value) {
                    this.value = value;
                };
            }
            '''
        ).strip()
        assert _decompose_java_class_from_string(
            content=content,
            strength='strong',
        ) == {
            'num_components': 1,
            'field_names': ['value'],
            'method_names': [],
        }

    def test_class_with_one_attribute(self) -> None:
        content = dedent(
            '''\
            class Dummy {
                private int i;
            }
            '''
        ).strip()
        assert _decompose_java_class_from_string(
            content=content,
            strength='strong',
        ) == {
            'num_components': 1,
            'field_names': ['i'],
            'method_names': [],
        }

    def test_class_with_two_attributes_defined_on_one_line(self) -> None:
        content = dedent(
            '''\
            class Dummy {
                private int i, j;
            }
            '''
        ).strip()
        assert _decompose_java_class_from_string(
            content=content,
            strength='strong',
        ) == {
            'num_components': 2,
            'field_names': ['i', 'j'],
            'method_names': [],
        }

    def test_class_with_two_attributes_defined_on_two_lines(self) -> None:
        content = dedent(
            '''\
            class Dummy {
                private int first;
                public double second;
            }
            '''
        ).strip()
        assert _decompose_java_class_from_string(
            content=content,
            strength='strong',
        ) == {
            'num_components': 2,
            'field_names': ['first', 'second'],
            'method_names': [],
        }

    def test_class_with_one_attribute_and_one_method(self) -> None:
        content = dedent(
            '''\
            class Dummy {
                private int i;
                public void print(String inputString) {
                    System.out.println(inputString);
                };
            }
            '''
        ).strip()
        assert _decompose_java_class_from_string(
            content=content,
            strength='strong',
        ) == {
            'num_components': 2,
            'field_names': ['i'],
            'method_names': ['print'],
        }

    def test_class_with_two_methods(self) -> None:
        content = dedent(
            '''\
            class Dummy {
                public void printOk() {
                    System.out.println("OK");
                };
                public void printNotOk() {
                    System.out.println("Not OK");
                };
            }
            '''
        ).strip()
        assert _decompose_java_class_from_string(
            content=content,
            strength='strong',
        ) == {
            'num_components': 2,
            'field_names': [],
            'method_names': ['printOk', 'printNotOk'],
        }

    def test_class_with_two_attributes_and_setter(self) -> None:
        content = dedent(
            '''\
            class Dummy {
                private int i;
                private int value;
                public void setValue(int value) {
                    this.value = value;
                };
            }
            '''
        ).strip()
        assert _decompose_java_class_from_string(
            content=content,
            strength='strong',
        ) == {
            'num_components': 3,
            'field_names': ['i', 'value'],
            'method_names': ['setValue'],
        }

    def test_class_with_two_attributes_and_setter_ignored(self) -> None:
        content = dedent(
            '''\
            class Dummy {
                private int i;
                private int value;
                public void setValue(int value) {
                    this.value = value;
                };
            }
            '''
        ).strip()
        assert _decompose_java_class_from_string(
            content=content,
            strength='strong',
            ignore_setters=True,
        ) == {
            'num_components': 3,
            'field_names': ['i', 'value'],
            'method_names': [],
        }

    def test_class_with_one_attribute_and_getter(self) -> None:
        content = dedent(
            '''\
            class Dummy {
                private int value;
                public int getValue() {
                    return value;
                };
            }
            '''
        ).strip()
        assert _decompose_java_class_from_string(
            content=content,
            strength='strong',
        ) == {
            'num_components': 2,
            'field_names': ['value'],
            'method_names': ['getValue'],
        }

    def test_class_with_one_attribute_and_getter_ignored(self) -> None:
        content = dedent(
            '''\
            class Dummy {
                private int value;
                public int getValue() {
                    return value;
                };
            }
            '''
        ).strip()
        assert _decompose_java_class_from_string(
            content=content,
            strength='strong',
            ignore_getters=True,
        ) == {
            'num_components': 2,
            'field_names': ['value'],
            'method_names': [],
        }

    def test_class_with_local_variable_declaration(self) -> None:
        content = dedent(
            '''\
            class Dummy {
                public void doNothing() {
                    String empty = "";
                };
            }
            '''
        ).strip()
        assert _decompose_java_class_from_string(
            content=content,
            strength='strong',
            ignore_getters=True,
        ) == {
            'num_components': 1,
            'field_names': [],
            'method_names': ['doNothing'],
        }


def _decompose_java_class_from_string(
    content: str,
    strength: Literal['strong', 'weak'],
    ignore_getters=False,
    ignore_setters=False,
) -> dict:
    ast = AST.build_from_javalang(build_ast_from_string(content))
    classes_ast = [
        ast.subtree(node)
        for node in ast.root().types
        if node.node_type == ASTNodeType.CLASS_DECLARATION
    ]
    assert len(classes_ast) == 1, 'String content must have exactly one class declaration'
    components = decompose_java_class(
        classes_ast[0],
        strength=strength,
        ignore_getters=ignore_getters,
        ignore_setters=ignore_setters,
    )
    return {
        'num_components': len(components),
        'field_names': _field_names(components),
        'method_names': _method_names(components),
    }


def _field_names(components: list[AST]) -> list[str]:
    result = set()
    for component in components:
        for field_declaration in component.proxy_nodes(ASTNodeType.FIELD_DECLARATION):
            for name in field_declaration.names:
                result.add(name)
    return sorted(result)


def _method_names(components: list[AST]) -> list[str]:
    return flatten(
        [
            [x.name for x in c.proxy_nodes(ASTNodeType.METHOD_DECLARATION)]
            for c in components
        ],
    )
