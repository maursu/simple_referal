make run:
	python manage.py runserver

make migrate:
	python manage.py makemigrations
	python manage.py migrate

make admin:
	python manage.py createsuperuser
