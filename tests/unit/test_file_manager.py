"""
test_file_manager.py

Unit tests for LocalStorageFileManager from file_manager.py.
"""

from app.core.file_manager import LocalStorageFileManager
import unittest
from tests.test_settings import TestSettings
import os
import shutil
from app.exceptions.exceptions import AppError

class TestLocalStorageFileManager(unittest.TestCase):

    def setUp(self):
        self.settings = TestSettings.generate()
        self.fm = LocalStorageFileManager(self.settings)

    def tearDown(self):
        shutil.rmtree(self.settings.TEMP_DIR_INPUT)
        shutil.rmtree(self.settings.TEMP_DIR_OUTPUT)

    def test_get_tmp_dir(self):
        """"
        Happy path: get_tmp_dir returns correct directory
        """
        returndir = self.fm.get_tmp_dir('output')
        self.assertEqual(returndir, self.settings.TEMP_DIR_OUTPUT)


    def test_wrong_get_tmp_dir(self):
        """
        Unhappy path: invalid type raises error
        """

        with self.assertRaises(AppError) as context:
            self.fm.get_tmp_dir("testtype")
        self.assertEqual(context.exception.code, "WRONG_TYPE")

    def test_create_tmp_file_path(self):
        """
        Creates tmp file with specified filename
        """

        ext = "wav"
        filename = "test"
        returndir, filename = self.fm.create_tmp_file_path(ext, "output", filename)
        self.assertEqual(returndir, os.path.join(self.settings.TEMP_DIR_OUTPUT, f"{filename}.{ext}"))


    def test_filename_create_tmp_file_path(self):
        """
        Creates tmp file with auto-generated filename
        """

        ext = "wav"
        returndir, filename = self.fm.create_tmp_file_path(ext, "output")
        self.assertTrue(filename)
        self.assertTrue(returndir.startswith(self.settings.TEMP_DIR_OUTPUT))


    
    def test_save(self):
        """
        Saves file to media folder
        """

        filename = "testfile.txt"
        filepath = os.path.join(self.settings.TEMP_DIR_OUTPUT, filename)
        with open(filepath, "w") as f:
            f.write("Some test content")
        returndir = self.fm.save(filepath, filename)
        self.assertEqual(returndir, f"{self.settings.MEDIA_DIR.rstrip('/')}/{filename}")


#python -m unittest discover -s tests -p "*.py" -v
