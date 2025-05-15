#!/bin/bash
echo "BUILD START"

# Install dependencies to Vercel's expected location
python -m pip install --upgrade pip
python -m pip install -r ./requirements/prod.txt --target ./.vercel/python

# Set Python path (crucial for Django to find packages)
export PYTHONPATH=$PYTHONPATH:$(pwd)/.vercel/python

# Verify Django is installed
python -c "import django; print(django.__version__)"

# Collect static files
python manage.py collectstatic --noinput --clear

echo "BUILD END"