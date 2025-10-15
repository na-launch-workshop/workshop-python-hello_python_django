# Django Hello World Translation Service

This project recreates the FastAPI translation sample using Django. It exposes a single endpoint that returns a localized greeting with an ISO-8601 timestamp appended.

## Prerequisites
- Python 3.10 or newer
- pip

## Installation
Create a virtual environment and install the development dependencies:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

## Running the Tests
```bash
python -m pytest
```

## Starting the Service
```bash
python manage.py runserver
```
The server listens on port `8080` by default. Override the `PORT` environment variable if needed.

## HTTP Endpoint
- `GET /` – Responds with a greeting string such as `hello world @ 2024-06-01T12:34:56+00:00`.

## Configuration
Environment variables provide the same configurability as the FastAPI version:
- `TRANSLATION_DEFAULT_LANGUAGE` (default: `EN`) – Two-letter code used to choose the greeting.
- `TRANSLATION_FILE` (default: `translations.json`) – File located in the `resources/` directory that contains the greeting map.
- `PORT` (default: `8080`) – Port for the HTTP server.

All translations are stored in `resources/translations.json`, copied verbatim from the FastAPI project.
