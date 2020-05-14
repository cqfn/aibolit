import os
from unittest import TestCase
from aibolit.config import Config


class TestConfig(TestCase):
    def test_java_files_folder_os_env(self):
        os.environ.setdefault('JAVA_FILES_PATH', '/test/path')
        assert Config.java_files_folder() == '/test/path'

    def test_java_files_folder_not_defined(self):
        assert Config.java_files_folder() is None
