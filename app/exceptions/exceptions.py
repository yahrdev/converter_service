"""
exceptions.py

Custom exception class for the service.
"""

from app.exceptions.errors import ERROR_MESSAGES

class AppError(Exception):
    def __init__(self, code, **kwargs):
        self.code = code
        self.message = ERROR_MESSAGES.get(code).format(**kwargs)
        super().__init__(self.message)