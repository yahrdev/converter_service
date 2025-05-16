"""
convertor.py

Abstract base class for file converters.

"""

from abc import ABC, abstractmethod
import magic
from pydub import AudioSegment
from tqdm import tqdm
from app.core.file_manager import get_file_manager
import os
from app.services.error_logger import log_exceptions
from app.exceptions.exceptions import AppError



class Convertor(ABC):

    def __init__(self, settings, file_manager=None):
        self.file_manager = file_manager or get_file_manager(settings)
        self._settings = settings

    @classmethod
    @abstractmethod
    def supports(cls):

        """List of supported (from, to) extension pairs."""

        pass

    @abstractmethod
    def convert(self, input_path: str, extension_from: str, filename: str, extension_to: str) -> str:
        """
            Returns:
            str: Full path to the converted output file.
        """
        pass

    def precheck_file(self, path: str, expected_ext: str):

        """ Validations before the conversion."""

        if not os.path.exists(path):
            raise AppError("FILE_NOT_FOUND_PATH", path=path)
        ext = extract_extension(path)
        if ext != expected_ext:
            raise AppError("EXTENSION_MISMATCH", ext=ext, expected=expected_ext)



class ConvertVideoAudio(Convertor):

    """Converts video to audio"""

    def __init__(self, settings, file_manager=None):
        super().__init__(settings, file_manager)

    @classmethod
    def supports(cls):
        return [
            ("mp4", "mp3"),
            ("mp3", "wav"),
            ("mp4", "wav"),
            ("wav", "mp3"),
        ]


    @log_exceptions
    def convert(self, input_path: str, extension_from: str, filename: str, extension_to: str) -> str:
 
        self.precheck_file(path = input_path, expected_ext=extension_from)
        SHOW_PROGRESS = self._settings.DEBUG_PROGRESS.lower() == "true"

        self.check_mediafile(input_path)
        (output_path, _) = self.file_manager.create_tmp_file_path(extension_to, type="output", filename=filename)
        chunk_size = 10_000
        audio = AudioSegment.from_file(input_path)
        AudioSegment.converter = self.file_manager.get_ffmpeg_path()

        # General duration
        total_duration = len(audio)

        # Init empty object
        processed_audio = AudioSegment.empty()

        # For showing progress on backend (for debug only)
        iterator = range(0, total_duration, chunk_size)
        if SHOW_PROGRESS:
            iterator = tqdm(iterator, desc="Convertation", unit="chunk")

        # Process video by parts
        for start in iterator:
            end = min(start + chunk_size, total_duration)
            chunk = audio[start:end]  
            processed_audio += chunk  # Cut a part and add to the final audio object

        # export to the file
        with open(output_path, "wb") as f:
            processed_audio.export(f, format=extension_to)
        if SHOW_PROGRESS:
            print("\n Finished:", output_path)
        return output_path
        
    @log_exceptions
    def check_mediafile(self, path: str):

        """check whether the file is audio or video"""

        mime = magic.from_file(path, mime=True)       
        if not (mime.startswith("audio/") or mime.startswith("video/")):
            raise AppError("FILE_WRONG_TYPE", path = path)
        


@log_exceptions
def get_convertator(extension_from: str, extension_to: str, settings) -> Convertor:
    from app.core.conversion_registry import ConversionRegistry
    convertor_cls = ConversionRegistry.get_convertor(extension_from, extension_to)
    if not convertor_cls:
        raise AppError("WRONG_CONVERSION", from_ext = extension_from, to_ext = extension_to)
    return convertor_cls(settings=settings)



def extract_extension(path: str) -> str:

    """extract extension from the provided path"""

    ext = os.path.splitext(path)[1]
    ext = ext.lstrip(".")
    if ext == "":
        raise AppError("INVALID_FILE_PATH", path = path)
    return ext
