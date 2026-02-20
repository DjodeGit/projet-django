#!/bin/bash
# Build script for Railway
pip install -r requirements.txt
python manage.py migrate --noinput
python manage.py collectstatic --noinput
