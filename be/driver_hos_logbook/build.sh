#!/usr/bin/env bash
# exit on error
set -o errexit

# Install poetry
pip install poetry

# Install dependencies
poetry install --no-root

# Run migrations
poetry run python manage.py migrate
