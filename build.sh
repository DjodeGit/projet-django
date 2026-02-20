#!/bin/bash
# Build script for Render
pip install -r requirements.txt
python manage.py collectstatic --noinput
