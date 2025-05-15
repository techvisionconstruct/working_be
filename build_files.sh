#!/bin/bash
echo "BUILD START"
python3.12 -m venv .venv
source .venv/bin/activate
# Install dependencies to Vercel's preferred location
python3.12 -m pip install -r ./requirements/prod.txt

# Ensure Python can find the packages
# export PYTHONPATH=$PYTHONPATH:$(pwd)/.vercel/python

# Collect static files with correct Python path
python3.12 -m pip install --upgrade pip
python3.12 manage.py collectstatic --noinput --clear
python3.12 -m pip list

echo "BUILD END"