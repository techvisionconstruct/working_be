.PHONY: dev run migrate makemigrations shell test

dev:
	python manage.py runserver_plus 0.0.0.0:8000 --print-sql

run:
	python manage.py runserver 0.0.0.0:8000

migrate:
	python manage.py migrate

migrations:
	python manage.py makemigrations

shell:
	python manage.py shell_plus --ipython

test:
	python manage.py test

create-superuser:
	python manage.py createsuperuser
