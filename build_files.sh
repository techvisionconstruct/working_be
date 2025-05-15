#!/bin/bash
echo "BUILD START"

# Install dependencies to Vercel's expected location
python3.12 -m pip install --upgrade pip
python3.12  -m pip install -r ./requirements/prod.txt --target ./.vercel/python

# Set Python path (crucial for Django to find packages)
export PYTHONPATH=$PYTHONPATH:$(pwd)/.vercel/python

# Verify Django is installed
python3.12  -c "import django; print(django.__version__)"

# Collect static files
python3.12 manage.py collectstatic --noinput --clear

echo "BUILD END"