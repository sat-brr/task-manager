install:
	poetry install
run:
	gunicorn -w 4 -b 0.0.0.0:8000 task_manager.wsgi:application
test:
	python3 manage.py test
lint:
	poetry run flake8 task_manager
migrations:
	poetry run python3 manage.py makemigrations
	poetry run python3 manage.py migrate
test-coverage:
	poetry run coverage run --source='.' manage.py test

	poetry run coverage report

	poetry run coverage xml
