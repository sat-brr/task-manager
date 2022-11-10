install:
	poetry install
start:
	python3 manage.py runserver
test:
	python3 manage.py test
lint:
	poetry run flake8 task_manager