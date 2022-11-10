all: install makemigrations migrate collectstatic

install:
	pip install -r requirements.txt

makemigrations:
	python manage.py makemigrations	--noinput

migrate:
	python manage.py migrate --noinput


collectstatic:
	python manage.py collectstatic --noinput