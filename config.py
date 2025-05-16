"""
config.py

The module for reading configurations
"""
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def abs_path(value: str) -> str:
    return value if os.path.isabs(value) else os.path.join(BASE_DIR, value)

class Settings:
    TEMP_DIR_INPUT = abs_path(os.getenv("TEMP_DIR_INPUT", "tmp/input"))  # Temporary folder to save the file after converting
    TEMP_DIR_OUTPUT = abs_path(os.getenv("TEMP_DIR_OUTPUT", "tmp/output"))  # Temporary folder to save the file after converting
    MEDIA_DIR = os.getenv("MEDIA_DIR", "/files")     # The folder to save the converted file to be served to the user
    MEDIA_FOLDER = abs_path(os.getenv("MEDIA_FOLDER", "files"))  
    TOOLS_FOLDER = abs_path(os.getenv("TOOLS_FOLDER", "tools"))  # The folder for saving executables like ffmpeg for converting
    STORAGE_TYPE = os.getenv("STORAGE_TYPE", "local")   # Where files are saved currently
    DOCS_DIR = abs_path(os.getenv("DOCS_DIR", "docs"))  # The directory for documentation (YAML files)
    DEBUG_PROGRESS = os.getenv("DEBUG_PROGRESS", "false")  # Whether to show debug progress or not

settings = Settings()