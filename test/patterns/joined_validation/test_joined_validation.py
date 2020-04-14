
import os
from unittest import TestCase
from aibolit.patterns.joined_validation.joined_validation import JoinedValidation
from pathlib import Path


class TestJoinedValidation(TestCase):
    dir_path = Path(os.path.realpath(__file__)).parent

    def test_canFindSimpleJoinedValidation(self):
        self.assertEqual(
            [3],
            JoinedValidation(Path(self.dir_path, 'SimpleJoinedValidation.java')).value(),
            'Could not find simple joined validation'
        )

    def test_canFindJoinedValidationAndOr(self):
        self.assertEqual(
            [3],
            JoinedValidation(Path(self.dir_path, 'JoinedValidationAndOr.java')).value(),
            'Could not find joined validation in AndOr condition'
        )

    def test_canFindJoinedValidationOrAnd(self):
        self.assertEqual(
            [3],
            JoinedValidation(Path(self.dir_path, 'JoinedValidationOrAnd.java')).value(),
            'Could not find joined validation in OrAnd condition'
        )

    def test_canFindJoinedValidationOrOr(self):
        self.assertEqual(
            [3],
            JoinedValidation(Path(self.dir_path, 'JoinedValidationOrOr.java')).value(),
            'Could not find joined validation in OrOr condition'
        )

    def test_canFindJoinedValidationOrFunctionCall(self):
        self.assertEqual(
            [8],
            JoinedValidation(Path(self.dir_path, 'JoinedValidationOrFunctionCall.java')).value(),
            'Could not find joined validation in function call'
        )

    def test_canFindJoinedValidationOrFieldAccess(self):
        self.assertEqual(
            [6],
            JoinedValidation(Path(self.dir_path, 'JoinedValidationOrFieldAccess.java')).value(),
            'Could not find joined validation in field access'
        )

    def test_canFindNoBracketsJoinedValidation(self):
        self.assertEqual(
            [3],
            JoinedValidation(Path(self.dir_path, 'NoBracketsJoinedValidation.java')).value(),
            'Could not find joined validation when using no brackets'
        )

    def test_canSkipEmptyJoinedValidation(self):
        self.assertEqual(
            [],
            JoinedValidation(Path(self.dir_path, 'EmptyJoinedValidation.java')).value(),
            'Could not skip empty joined validation'
        )

    def test_canSkipNoJoinedValidation(self):
        self.assertEqual(
            [],
            JoinedValidation(Path(self.dir_path, 'NoJoinedValidation.java')).value(),
            'Could not skip when there is no joined validation'
        )
