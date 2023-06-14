### Project tests and linter status:
[![flake8](https://github.com/sat-brr/task-manager/actions/workflows/flake8.yml/badge.svg)](https://github.com/sat-brr/task-manager/actions/workflows/flake8.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/965e3cf390a26562b40b/maintainability)](https://codeclimate.com/github/sat-brr/python-project-52/maintainability)
[![tests](https://github.com/sat-brr/task-manager/actions/workflows/tests.yml/badge.svg)](https://github.com/sat-brr/task-manager/actions/workflows/tests.yml)
[![Test Coverage](https://api.codeclimate.com/v1/badges/965e3cf390a26562b40b/test_coverage)](https://codeclimate.com/github/sat-brr/python-project-52/test_coverage)

# Task Manager

## Description:
This is a web application that allows you to track scheduled tasks, as well as assign them statuses and labels for easy tracking.

### Implemented:
- User registration and authorization
- Creating statuses and labels
- Creating tasks, as well as assigning statuses and labels to them
- Deleting users, tasks, statuses, and labels
- Error tracking in Rollbar
- Russian and English localizations
- The application works with PostgreSQL

## Installation and launch without Docker:

### Install:
```
pip install poetry
git clone https://github.com/sat-brr/task-manager.git
make install
```

#### Environment variables:
Create .env file in the root of the project and specify the variables:
- DEBUG = True/False starting in debug mode or not
- DATABASE_URL = URL to DB in the format postgresql://user:password@server:port/dbname
- SECRET_KEY = Your django secret key
- ROLLBAR_TOKEN = Your rollbar token
- POSTGRES_DB=test
- POSTGRES_USER=test123
- POSTGRES_PASSWORD=test321

#### Perform migration:
```
make migrations
```

#### Select a language:
Open the file task_manager/settings.py and change the value of the LANGUAGE_CODE variable to 'ru' for Russian localization or 'en' for English.

### Launch:
```
make run
```

## Installation and launch with Docker:

### Clone the repository:
```
git clone https://github.com/sat-brr/task-manager.git
```

#### Environment variables:
Create .env file in the root of the project:
```
cd task-manager/
touch .env
```
Specify variables:
- DEBUG = True/False starting in debug mode or not
- SECRET_KEY = Your django secret key
- ROLLBAR_TOKEN = Your rollbar token
- POSTGRES_DB=test
- POSTGRES_USER=test123
- POSTGRES_PASSWORD=test321

#### Select a language:
Open the file task_manager/settings.py and change the value of the LANGUAGE_CODE variable to 'ru' for Russian localization or 'en' for English.

### Build containers:
```
cd task-manager/
sudo docker-compose build
```

### Launch:
```
sudo docker-compose up
```