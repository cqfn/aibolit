import os
from unittest import TestCase
from pathlib import Path
from aibolit.patterns.array_as_argument.array_as_argument import ArrayAsArgument


class TestArrayAsArgument(TestCase):
    dir_path = Path(os.path.realpath(__file__)).parent
    pattern = ArrayAsArgument()

    def test_NoArgument(self):
        file = Path(self.dir_path, 'NoArgument.java')
        self.assertEqual(
            [],
            self.pattern.value(file),
            'Should not match no argument method'
        )

    def test_PrimitiveAsArgument(self):
        file = Path(self.dir_path, 'PrimitiveAsArgument.java')
        self.assertEqual(
            [],
            self.pattern.value(file),
            'Should not match method with primitive as argument'
        )

    def test_ArrayAsArgument(self):
        file = Path(self.dir_path, 'ArrayAsArgument.java')
        self.assertEqual(
            [2],
            self.pattern.value(file),
            'Should match method with array as argument'
        )

    def test_ObjectAsArgument(self):
        file = Path(self.dir_path, 'ObjectAsArgument.java')
        self.assertEqual(
            [],
            self.pattern.value(file),
            'Should not match method with object as argument'
        )

    def test_PrimitiveAndArrayAsArgument(self):
        file = Path(self.dir_path, 'PrimitiveAndArrayAsArgument.java')
        self.assertEqual(
            [2],
            self.pattern.value(file),
            'Should match method with array as argument'
        )

    def test_GenericArrayAsArgument(self):
        file = Path(self.dir_path, 'GenericArrayAsArgument.java')
        self.assertEqual(
            [2],
            self.pattern.value(file),
            'Should match method with generic array as argument'
        )

    def test_ConstructorWithArrayAsArgument(self):
        file = Path(self.dir_path, 'ConstructorWithArrayAsArgument.java')
        self.assertEqual(
            [2],
            self.pattern.value(file),
            'Should match constructor with array as argument'
        )
