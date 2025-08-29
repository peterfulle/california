#!/usr/bin/env bash
# exit on error
set -o errexit

# Install Python dependencies
pip install -r requirements.txt

# Apply database migrations
python manage.py migrate

# Create default industries
echo "Creating default industries..."
python manage.py create_industries

# Collect static files
python manage.py collectstatic --no-input
