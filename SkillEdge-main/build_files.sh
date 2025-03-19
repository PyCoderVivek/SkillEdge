#!/bin/bash
# Build script for Vercel deployment

# Install Python dependencies
pip install -r requirements.txt

# Make migrations and collect static files
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput 