import os
from unittest import TestCase
from pathlib import Path
from aibolit.patterns.array_as_argument.array_as_argument import ArrayAsArgument


class TestArrayAsArgument(TestCase):
    dir_path = Path(os.path.realpath(__file__)).parent

    def test_NoArgument(self):
        self.assertEqual(
            [],
            ArrayAsArgument(Path(self.dir_path, 'NoArgument.java')).value(),
            'Should not match no argument method'
        )

    def test_PrimitiveAsArgument(self):
        self.assertEqual(
            [],
            ArrayAsArgument(Path(self.dir_path, 'PrimitiveAsArgument.java')).value(),
            'Should not match method with primitive as argument'
        )

    def test_ArrayAsArgument(self):
        self.assertEqual(
            [2],
            ArrayAsArgument(Path(self.dir_path, 'ArrayAsArgument.java')).value(),
            'Should match method with array as argument'
        )

    def test_ObjectAsArgument(self):
        self.assertEqual(
            [],
            ArrayAsArgument(Path(self.dir_path, 'ObjectAsArgument.java')).value(),
            'Should not match method with object as argument'
        )

    def test_PrimitiveAndArrayAsArgument(self):
        self.assertEqual(
            [2],
            ArrayAsArgument(Path(self.dir_path, 'PrimitiveAndArrayAsArgument.java')).value(),
            'Should match method with array as argument'
        )

    def test_GenericArrayAsArgument(self):
        self.assertEqual(
            [2],
            ArrayAsArgument(Path(self.dir_path, 'GenericArrayAsArgument.java')).value(),
            'Should match method with generic array as argument'
        )
