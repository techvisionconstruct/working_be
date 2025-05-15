#!/bin/bash
echo "BUILD START"

# Install dependencies to Vercel's expected location
python3.12 -m pip install --upgrade pip
python3.12  -m pip install -r ./requirements/prod.txt --target ./.vercel/python

# Critical: Set Python path for runtime
echo "PYTHONPATH=$(pwd)/.vercel/python" >> .env
# Verify Django is accessible
python -c "import django; print(f'Django version: {django.__version__}')" || exit 1

# Collect static files
python3.12 manage.py collectstatic --noinput --clear

echo "BUILD END"