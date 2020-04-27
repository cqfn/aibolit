import os.path
from pathlib import Path
from unittest import TestCase

from aibolit.patterns.assert_in_code.assert_in_code import AssertInCode


class TestAssertInCode(TestCase):
    cur_file_dir = Path(os.path.realpath(__file__)).parent

    def test_assert_in_code(self):
        file = Path(self.cur_file_dir, 'Book.java')
        self.assertEqual(AssertInCode().value(file), [3])

    def test_AssembleDockingAction(self):
        file = Path(self.cur_file_dir, 'AssembleDockingAction.java')
        self.assertEqual(AssertInCode().value(file), [320])

    def test_AssembleDualTextFiel(self):
        file = Path(self.cur_file_dir, 'AssemblyDualTextField.java')
        self.assertEqual(AssertInCode().value(file), [569])

    def test_Assertions(self):
        file = Path(self.cur_file_dir, 'Assertions.java')
        self.assertEqual(AssertInCode().value(file), [42])

    def test_ElasticSearchNodesSniffer(self):
        file = Path(self.cur_file_dir, 'ElasticSearchNodesSniffer.java')
        self.assertEqual(AssertInCode().value(file), [120, 274, 276])

    def test_GetAliasesResponse(self):
        file = Path(self.cur_file_dir, 'GetAliasesResponse.java')
        self.assertEqual(AssertInCode().value(file), [169, 170])

    def test_HighlightBuilder(self):
        file = Path(self.cur_file_dir, 'HighlightBuilder.java')
        self.assertEqual(AssertInCode().value(file), [128, 472])

    def test_InternalChannelz(self):
        file = Path(self.cur_file_dir, 'InternalChannelz.java')
        self.assertEqual(AssertInCode().value(file), [81, 108, 116, 117, 140, 239, 244])

    def test_Metadata(self):
        file = Path(self.cur_file_dir, 'Metadata.java')
        self.assertEqual(AssertInCode().value(file), [141])

    def test_NettyServerHandler(self):
        file = Path(self.cur_file_dir, 'NettyServerHandler.java')
        self.assertEqual(AssertInCode().value(file), [356, 364])

    def test_packageinfo(self):
        file = Path(self.cur_file_dir, 'package-info.java')
        self.assertEqual(AssertInCode().value(file), [])

    def test_Reindexer(self):
        file = Path(self.cur_file_dir, 'Reindexer.java')
        self.assertEqual(AssertInCode().value(file), [188, 204, 214, 233])

    def test_Sniffer(self):
        file = Path(self.cur_file_dir, 'Sniffer.java')
        self.assertEqual(AssertInCode().value(file), [148])

    def test_Status(self):
        file = Path(self.cur_file_dir, 'Status.java')
        self.assertEqual(AssertInCode().value(file), [663])
