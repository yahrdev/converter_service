"""
test_settings.py

Creates isolated temporary settings for use in tests.
"""


import tempfile
import os

class TestSettings:
    @staticmethod
    def generate():   # to create unique temporary folders for each test to ensure isolation.
        class _Settings:
            TEMP_DIR_INPUT = tempfile.mkdtemp()
            TEMP_DIR_OUTPUT = tempfile.mkdtemp()
            MEDIA_FOLDER = tempfile.mkdtemp()
            TOOLS_FOLDER = tempfile.mkdtemp()
            MEDIA_DIR = "/media"
            STORAGE_TYPE = "local"
            DEBUG_PROGRESS = "False"
            DOCS_DIR = os.path.abspath("docs")
        return _Settings()
