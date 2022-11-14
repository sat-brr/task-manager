install:
	poetry install
start:
	python3 manage.py runserver 127.0.0.1:8001
test:
	python3 manage.py test
lint:
	poetry run flake8 task_manager
migrations:
	poetry run python3 manage.py makemigrations
	poetry run python3 manage.py migrate