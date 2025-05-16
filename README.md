# 🎧 converter_service

**This microservice converts files (for example, from mp4 to wav) and is built with architecture that’s easy to test and extend.**

The design follows SOLID principles and separates logic into small, focused parts:
- File handling
- Conversion logic
- API layer
- Error handling
  
This makes it easier to change or add new features, like supporting other file types (e.g., txt → pdf). The service also includes unit and integration tests and returns clear error messages when something goes wrong.

You can use it as a standalone tool or integrate it into a bigger system.

---

## Features

- Video-to-audio conversion (`.mp4`, `.avi`, etc. → `.wav`)
- Easily extendable conversion logic (e.g., `txt → pdf`)
- Centralized error handling with structured responses
- Pluggable file manager (supports local filesystem; S3-ready)
- Test coverage: unit + integration
- Flask-based API with Swagger documentation

---


## Running locally

# Set up virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run the service
python app/main.py


## Run tests

# Unit tests
python -m unittest discover -s tests/unit -p "*.py"

# Integration tests
pytest tests/integration

Once the app is running, open in browser:
http://localhost:5000/apidocs/
