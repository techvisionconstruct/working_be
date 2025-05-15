#!/bin/bash
echo "BUILD START"
python3.12 -m pip install --upgrade pip
python3.12 -m pip install -r requirements/prod.txt --target ./.vercel/python
python manage.py collectstatic --noinput --clear
echo "BUILD END"