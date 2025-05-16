"""
swagger_description.py

Helper script for Swagger documentation auto-generation. Optional.
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.exceptions.errors import ERROR_MESSAGES, STATUS_MAP
import re

TEMPLATE_PATH = "docs/swagger_template.yml"

def generate_markdown_table():
    header = "| Code | HTTP Status | Message |\n|------|--------------|---------|\n"
    rows = []
    for code, message in ERROR_MESSAGES.items():
        status = STATUS_MAP.get(code, "❓")
        rows.append(f"| `{code}` | {status} | {message} |")
    return header + "\n".join(rows)

def insert_table_into_yaml():
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    table = generate_markdown_table()
    indented_table = "  " + table.replace("\n", "\n  ")
    new_description = re.sub(
        r"(description:\s*\|)(.*?)(?=(\n\w|\Z))",
        f"\\1\n  This API converts media files between formats.\n\n  ### Error Codes\n{indented_table}",
        content,
        flags=re.DOTALL
    )

    with open(TEMPLATE_PATH, "w", encoding="utf-8") as f:
        f.write(new_description)

if __name__ == "__main__":
    insert_table_into_yaml()