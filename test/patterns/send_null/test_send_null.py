import os
from unittest import TestCase
from aibolit.patterns.send_null.send_null import SendNull
from pathlib import Path


class TestSendNull(TestCase):
    dir_path = Path(os.path.realpath(__file__)).parent
    method_send_null_finder = SendNull()

    def test_one_send(self):
        lines = self.method_send_null_finder.value(Path(self.dir_path, 'BaseKeyframeAnimation.java'))
        self.assertEqual(lines, [146])

    def test_multi_level_invocation(self):
        lines = self.method_send_null_finder.value(Path(self.dir_path, 'Configuration.java'))
        self.assertEqual(lines, [379, 442, 549, 638, 656, 830, 866, 1362, 2393, 2874, 2988, 3080, 3492, 3758, 3855])

    def test_no_null_methods(self):
        lines = self.method_send_null_finder.value(Path(self.dir_path, 'FillContent.java'))
        self.assertEqual(lines, [])

    def test_simple_invocation(self):
        lines = self.method_send_null_finder.value(Path(self.dir_path, 'FJIterateTest.java'))
        self.assertEqual(lines, [493])

    def test_more_method_invocations(self):
        lines = self.method_send_null_finder.value(Path(self.dir_path, 'SequenceFile.java'))
        self.assertEqual(lines, [1097, 1186, 1201, 1217, 3285, 3298, 3367, 3537, 3550])

    def test_constructor_send_null(self):
        lines = self.method_send_null_finder.value(Path(self.dir_path, 'Constructor.java'))
        self.assertEqual(lines, [5, 14, 15, 16, 17, 18])

    def test_super_in_constructor_with_ternary_operator(self):
        lines = self.method_send_null_finder.value(Path(self.dir_path, 'AclPermissionParam.java'))
        self.assertEqual(lines, [46, 50])

    def test_this_with_ternary_operator(self):
        lines = self.method_send_null_finder.value(Path(self.dir_path, 'AddOp.java'))
        self.assertEqual(lines, [44, 48])

    def test_super_in_constructor_with_method_inv(self):
        lines = self.method_send_null_finder.value(Path(self.dir_path, 'ByteArrayMultipartFileEditor.java'))
        self.assertEqual(lines, [49])
