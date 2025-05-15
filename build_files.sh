echo "BUILD START"
 python3.12 -m pip install -r ./requirements/prod.txt --target ./.vercel/python
 python3.12 manage.py collectstatic --noinput --clear
 echo "BUILD END"