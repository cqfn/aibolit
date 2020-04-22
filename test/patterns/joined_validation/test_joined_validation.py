import os
from unittest import TestCase
from aibolit.patterns.joined_validation.joined_validation import JoinedValidation
from pathlib import Path


class TestJoinedValidation(TestCase):
    dir_path = Path(os.path.realpath(__file__)).parent
    pattern = JoinedValidation()

    def test_canFindSimpleJoinedValidation(self):
        file = Path(self.dir_path, 'SimpleJoinedValidation.java')
        self.assertEqual(
            [3],
            self.pattern.value(file),
            'Could not find simple joined validation'
        )

    def test_canFindJoinedValidationAndOr(self):
        file = Path(self.dir_path, 'JoinedValidationAndOr.java')
        self.assertEqual(
            [3],
            self.pattern.value(file),
            'Could not find joined validation in AndOr condition'
        )

    def test_canFindJoinedValidationOrAnd(self):
        file = Path(self.dir_path, 'JoinedValidationOrAnd.java')
        self.assertEqual(
            [3],
            self.pattern.value(file),
            'Could not find joined validation in OrAnd condition'
        )

    def test_canFindJoinedValidationOrOr(self):
        file = Path(self.dir_path, 'JoinedValidationOrOr.java')
        self.assertEqual(
            [3],
            self.pattern.value(file),
            'Could not find joined validation in OrOr condition'
        )

    def test_canFindJoinedValidationOrFunctionCall(self):
        file = Path(self.dir_path, 'JoinedValidationOrFunctionCall.java')
        self.assertEqual(
            [8],
            self.pattern.value(file),
            'Could not find joined validation in function call'
        )

    def test_canFindJoinedValidationOrFieldAccess(self):
        file = Path(self.dir_path, 'JoinedValidationOrFieldAccess.java')
        self.assertEqual(
            [6],
            self.pattern.value(file),
            'Could not find joined validation in field access'
        )

    def test_canFindNoBracketsJoinedValidation(self):
        file = Path(self.dir_path, 'NoBracketsJoinedValidation.java')
        self.assertEqual(
            [3],
            self.pattern.value(file),
            'Could not find joined validation when using no brackets'
        )

    def test_canSkipEmptyJoinedValidation(self):
        file = Path(self.dir_path, 'EmptyJoinedValidation.java')
        self.assertEqual(
            [],
            self.pattern.value(file),
            'Could not skip empty joined validation'
        )

    def test_canSkipNoJoinedValidation(self):
        file = Path(self.dir_path, 'NoJoinedValidation.java')
        self.assertEqual(
            [],
            self.pattern.value(file),
            'Could not skip when there is no joined validation'
        )
