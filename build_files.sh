echo "BUILD START"
 python3.12 -m pip install -r ./requirements/prod.txt
 python3.12 manage.py collectstatic --noinput --clear
 echo "BUILD END"