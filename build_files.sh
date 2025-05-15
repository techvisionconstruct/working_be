#!/bin/bash
echo "BUILD START"
python -m pip install --upgrade pip
python -m pip install -r requirements/prod.txt --target ./.vercel/python
python manage.py collectstatic --noinput --clear
echo "BUILD END"