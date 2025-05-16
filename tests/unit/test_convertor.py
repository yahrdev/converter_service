"""
test_convertor.py

Unit tests for Convertor subclasses from convertor.py.
"""

import unittest
from app.core.convertor import ConvertVideoAudio
from app.core.file_manager import LocalStorageFileManager
from tests.test_settings import TestSettings
import shutil
import os
from app.exceptions.exceptions import AppError
import tests.shared_helpers.dummy_generators as dg

class TestConvertVideoAudio(unittest.TestCase):

    def setUp(self):
        self.settings = TestSettings.generate()
        self.fm = LocalStorageFileManager(self.settings)
        self.convertor = ConvertVideoAudio(self.settings, self.fm)


    def tearDown(self):
        shutil.rmtree(self.settings.TEMP_DIR_INPUT)
        shutil.rmtree(self.settings.TEMP_DIR_OUTPUT)
        shutil.rmtree(self.settings.MEDIA_FOLDER)


    def test_convert(self):
        """"
        Happy path: successful conversion
        """

        video_path = os.path.join(self.settings.TEMP_DIR_INPUT, "test.mp4")
        dg.create_dummy_video(video_path)
        output_file_path = ''
        output_file_path = self.convertor.convert(video_path, "mp4", "test", "wav")
        self.assertTrue(os.path.exists(output_file_path))
        self.assertTrue(output_file_path.endswith(".wav"))


    def test_wrong_extension_convert(self):
        """
        Unhappy path: extension mismatch
        """

        file_path = os.path.join(self.settings.TEMP_DIR_INPUT, "test_text.txt")
        output_file_path = ''
        with open(file_path, "w") as f:
            f.write("Some test content")  
        with self.assertRaises(AppError) as context:
            output_file_path = self.convertor.convert(file_path, "mp4", "test_text", "wav")
        self.assertEqual(context.exception.code, "EXTENSION_MISMATCH")
        self.assertEqual(output_file_path, '')


    def test_not_media_convert(self):
        """
        Unhappy path: file is not a valid media file
        """

        file_path = os.path.join(self.settings.TEMP_DIR_INPUT, "test_video.mp4")
        output_file_path = ''
        with open(file_path, "w") as f:
            f.write("Some test content")
        with self.assertRaises(AppError) as context:
            output_file_path = self.convertor.convert(file_path, "mp4", "test_video", "wav")
        self.assertEqual(context.exception.code, "FILE_WRONG_TYPE")
        self.assertEqual(output_file_path, '')

