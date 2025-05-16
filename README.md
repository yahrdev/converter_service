# 🎧 converter_service

**This microservice converts files (like mp4 to wav) and is easy to test, change, and grow**

It uses a clean and simple architecture, so the code is easy to read and extend. Errors are handled clearly, and tests are included. You can use this service alone or inside a bigger project.

---

## Features

- Video-to-audio conversion (`.mp4`, `.avi`, etc. → `.wav`)
- Easily extendable conversion logic (e.g., `txt → pdf`)
- Centralized error handling with structured responses
- Pluggable file manager (supports local filesystem; S3-ready)
- Test coverage: unit + integration
- Flask-based API with Swagger documentation

---

## Project structure

converter_service/
├── app/ # Main application logic
│ ├── api/ # Routers, schemas, handlers
│ ├── core/ # Core logic: convertors, file managers
│ ├── services/ # Utilities like logging
│ └── exceptions/ # Error types and handlers
├── docs/ # Swagger specs
├── tests/ # Unit and integration tests
├── config.py # Configuration
├── requirements.txt # Dependencies
└── main.py # Entry point



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
