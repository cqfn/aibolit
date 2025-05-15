# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

from unittest import TestCase, skip
from pathlib import Path

from aibolit.ast_framework.java_package import JavaPackage


@skip('JavaClassMethod is deprecated')
class JavaClassMethodTestCase(TestCase):
    def test_method_name(self):
        java_package = JavaPackage(Path(__file__).parent.absolute() / 'TwoClasses.java')
        java_class = java_package.java_classes['Second']
        self.assertEqual(java_class.methods.keys(), {'Decrement', 'Increment'})

    def test_used_methods(self):
        java_package = JavaPackage(
            Path(__file__).parent.absolute() / 'MethodUseOtherMethodExample.java'
        )
        java_class = java_package.java_classes['MethodUseOtherMethod']
        for method_name, methods in java_class.methods.items():
            with self.subTest(f'Method: {method_name}'):
                self.assertEqual(len(methods), 1)
                method = next(iter(methods))
                self.assertEqual(JavaClassMethodTestCase._used_methods_by_name[method_name],
                                 method.used_methods.keys())

    def test_method_parameters(self):
        java_package = JavaPackage(
            Path(__file__).parent.absolute() / 'MethodUseOtherMethodExample.java'
        )
        java_class = java_package.java_classes['MethodUseOtherMethod']
        for method_name, methods in java_class.methods.items():
            with self.subTest(f'Method: {method_name}'):
                self.assertEqual(len(methods), 1)
                method = next(iter(methods))
                self.assertEqual(JavaClassMethodTestCase._methods_parameters[method_name],
                                 method.parameters.keys())

    def test_used_fields(self):
        java_package = JavaPackage(
            Path(__file__).parent.absolute() / 'MethodUseOtherMethodExample.java'
        )
        java_class = java_package.java_classes['MethodUseOtherMethod']
        for method_name, methods in java_class.methods.items():
            with self.subTest(f'Method: {method_name}'):
                self.assertEqual(len(methods), 1)
                method = next(iter(methods))
                self.assertEqual(JavaClassMethodTestCase._used_fields_by_name[method_name],
                                 method.used_fields.keys())

    _used_methods_by_name = {
        'useOnlyMethods1': {'useOnlyMethods2'},
        'useOnlyMethods2': {'useOnlyMethods1'},
        'getField': set(),
        'setField': set(),
        'standAloneMethod': set(),
        'shadowing': set(),
    }

    _methods_parameters = {
        'useOnlyMethods1': {'x'},
        'useOnlyMethods2': {'x'},
        'getField': set(),
        'setField': {'value'},
        'standAloneMethod': set(),
        'shadowing': {'redundantField'},
    }

    _used_fields_by_name = {
        'useOnlyMethods1': set(),
        'useOnlyMethods2': set(),
        'getField': {'connectingField'},
        'setField': {'connectingField'},
        'standAloneMethod': set(),
        'shadowing': set(),
    }
