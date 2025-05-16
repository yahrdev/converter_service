"""
schemas.py

Data schemas and data validation

"""

from marshmallow import Schema, fields, post_load, validates
from marshmallow.validate import Length
from dataclasses import dataclass
from app.core.conversion_registry import ConversionRegistry
from app.exceptions.exceptions import AppError

@dataclass
class FilePath:

    """
    convert_file endpoint JSON
    """

    filepath: str
    output_filename: str
    original_extension: str
    target_extension: str



class FilePathSchema(Schema):
    filepath = fields.Str(required=True, validate=Length(min=1), data_key="filepath")
    output_filename = fields.Str(required=True, validate=Length(min=1), data_key="output_filename")
    original_extension = fields.Str(required=True, validate=Length(min=1), data_key="original_extension")
    target_extension = fields.Str(required=True, validate=Length(min=1), data_key="target_extension")

    @post_load
    def make_parametr(self, data, **kwargs):

        """
        Allows to work with schema fields instead of raw JSON.
        """

        return FilePath(**data)
    

    @validates("original_extension")
    def validate_original_extension(self, value):
        check_supported_extensions(value)
       
    
    @validates("target_extension")
    def validate_target_extension(self, value):
        check_supported_extensions(value)

    
@dataclass
class Message:
    message: any  
    code: str

class MessageSchema(Schema):
    message = fields.Raw(data_key="message")
    code = fields.Str(data_key="code")

    @post_load
    def make_parametr(self, data, **kwargs):
        return Message(**data)
    



def check_supported_extensions(value: str):
    """
    Check whether the received extensions are supported and correct.
    """
    supported_exts = ConversionRegistry.get_supported_extension_set()
    if value.lower() not in supported_exts:
        raise AppError("UNSUPPORTED_EXTENSION", value = value, supported = ', '.join(supported_exts))


