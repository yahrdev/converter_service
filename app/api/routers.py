"""
routers.py

The API routers. Details are provided in the Flasgger documentation.

"""


from flask import request, send_from_directory
from app.core.convertor import get_convertator
from app.core.file_manager import get_file_manager
from app.api.schemas import FilePathSchema
from flasgger import swag_from
import os


def register_routes(app, settings):
    @app.route("/transcriber/converter", methods = ['POST'])
    @swag_from(os.path.join(settings.DOCS_DIR, "convert_file.yml"))
    def convert_file():
        result = FilePathSchema().load(request.get_json())
        convertator = get_convertator(result.original_extension, result.target_extension, settings)
        converted_path = convertator.convert(result.filepath, result.original_extension, result.output_filename, result.target_extension)
        fm = get_file_manager(settings)
        result_path = fm.save(converted_path, f"{result.output_filename}.{result.target_extension}")
        fm.clear_tmp_folders()
        return result_path



    @app.route("/files/<filename>")
    @swag_from(specs = os.path.join(settings.DOCS_DIR, "serve_file.yml"))
    def serve_file(filename):
        return send_from_directory(settings.MEDIA_FOLDER, filename)