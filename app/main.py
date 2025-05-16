"""
main.py

Entry point for running the Flask application.

"""
from config import settings
from app import create_app

app = create_app(settings)


if __name__ == "__main__":
    app.run()

    #gunicorn -w 4 -b 0.0.0.0:5000 app:app
