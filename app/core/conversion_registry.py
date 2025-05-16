"""
conversion_registry.py

The module for gathering convertor data (supported extensions, conversions etc). 
It allows the list of supported operations to be generated dynamically based on the convertor.py code

"""


from app.core.convertor import Convertor
from typing import Type

class ConversionRegistry:
    _mapping = None

    @classmethod
    def get_mapping(cls) -> dict:
        """
        Gets a dict of all conversions that are supported by Convertor classes. 
        {
            ("mp4", "mp3"): ConvertVideoAudio,
            ("pdf", "txt"): ConvertPDF,
            ...
        }

        """
        if cls._mapping is None:
            cls._mapping = {}

        for convclass in Convertor.__subclasses__():
            for pair in convclass.supports():
                cls._mapping[pair] = convclass

        return cls._mapping
    

    @classmethod
    def get_convertor(cls, from_ext: str, to_ext: str) -> Type[Convertor]:
        """
        Gets class for specified pair
        """
        mapping = cls.get_mapping()
        return mapping.get((from_ext.lower(), to_ext.lower()))
    

    @classmethod
    def get_allowed_conversions_list(cls) -> list:
        """
        [
            ("mp3", "wav"),
            ("mp4", "mp3"),
            ...
        ]
        """
        return sorted(cls.get_mapping().keys())
    
    @classmethod
    def get_supported_extension_set(cls) -> set:
        return {ext for pair in cls.get_mapping() for ext in pair}




