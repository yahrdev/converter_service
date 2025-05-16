"""
file_manager.py

The module for processing received files from the endpoint.
"""


import os
import shutil
from typing import Tuple, Optional, List
from typing_extensions import Literal
import uuid
from abc import ABC, abstractmethod
import platform
from app.services.error_logger import log_exceptions
from app.exceptions.exceptions import AppError



class FileManager(ABC):

    def __init__(self, settings):
        self._settings = settings


    @abstractmethod
    def get_tmp_dir(self, type: Literal["input", "output"]) -> str:

        """Get or create a temporary directory."""

        pass
        
    @abstractmethod
    def create_tmp_file_path(self, extension: str, type: Literal["input", "output"], filename = None) -> Tuple[str, str]:
        """
        Returns:
            Tuple[tmp_path, filename (without extension)]
        """
        pass

    @abstractmethod
    def save(self, filepath: str, filename: str) -> str:

        """Save to the folder used for serving the file to a user."""

        pass
        
    @abstractmethod
    def clear_tmp_folders(self, folders: Optional[List[str]] = None):

        """Clear temporary folders after processing."""

        pass

    @abstractmethod
    def get_ffmpeg_path(self) -> str:

        """Additional exe files for the conversions"""

        pass



class LocalStorageFileManager(FileManager):

    """
    The class for managing files on local storage (e.g., D:/).
    """

    def __init__(self, settings):
        super().__init__(settings)

    @log_exceptions
    def get_tmp_dir(self, type: Literal["input", "output"]) -> str:
        workdir = ''
        if type == "input":
            workdir = self._settings.TEMP_DIR_INPUT
        if type == "output":
            workdir = self._settings.TEMP_DIR_OUTPUT
        if not type in ["input", "output"]:
            raise AppError("WRONG_TYPE", type = type)
        os.makedirs(workdir, exist_ok=True) #create workdir
        return workdir
        
    def create_tmp_file_path(self, extension: str, type: Literal["input", "output"], filename = None) -> Tuple[str, str]:
        """
        Returns:
            Tuple[tmp_path, filename (without extension)]
        """
        workdir = self.get_tmp_dir(type)
        if filename is None:
            filename = f"{uuid.uuid4()}"
        tmp_path = os.path.join(workdir, f"{filename}.{extension}")
        return tmp_path, filename  

    @log_exceptions
    def save(self, filepath: str, filename: str) -> str:
        media_folder = self._settings.MEDIA_FOLDER
        os.makedirs(media_folder, exist_ok=True) 
        target_path = os.path.join(media_folder, filename)
        shutil.copy(filepath, target_path)
        return f"{self._settings.MEDIA_DIR.rstrip('/')}/{filename}"
        

    def clear_tmp_folders(self):
        for filename in os.listdir(self._settings.TEMP_DIR_OUTPUT):
            filepath = os.path.join(self._settings.TEMP_DIR_OUTPUT, filename)
            try:
                if os.path.isfile(filepath) or os.path.islink(filepath):  #if it is a file or a symlink
                    os.remove(filepath)
                elif os.path.isdir(filepath):  #if it is a directory
                    shutil.rmtree(filepath)
            except Exception as e:
                print(f"Clearing error {filepath}: {e}")


    def get_ffmpeg_path(self) -> str:
        ffmpeg_binary = "ffmpeg.exe" if platform.system() == "Windows" else "ffmpeg"
        custom_path = os.path.join(self._settings.TOOLS_FOLDER, ffmpeg_binary)

        if os.path.exists(custom_path):
            return custom_path
        else:
            return ffmpeg_binary  # use system ffmpeg
    


file_manager_registry = {
    "local": LocalStorageFileManager
}

@log_exceptions
def get_file_manager(settings) -> FileManager:
    manager_class = file_manager_registry.get(settings.STORAGE_TYPE)
    if not manager_class:
        raise AppError("FILE_MANAGER_NOT_IMPLEMENTED", type=settings.STORAGE_TYPE)
    return manager_class(settings)
    



    
