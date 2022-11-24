### Hexlet tests and linter status:
[![Actions Status](https://github.com/sat-brr/python-project-52/workflows/hexlet-check/badge.svg)](https://github.com/sat-brr/python-project-52/actions)
[![pylint](https://github.com/sat-brr/python-project-52/actions/workflows/pylint.yml/badge.svg)](https://github.com/sat-brr/python-project-52/actions/workflows/pylint.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/965e3cf390a26562b40b/maintainability)](https://codeclimate.com/github/sat-brr/python-project-52/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/965e3cf390a26562b40b/test_coverage)](https://codeclimate.com/github/sat-brr/python-project-52/test_coverage)

# Task Manager

## Project on railway.app:
https://task-manager-sat.up.railway.app/

## Description:
This is a web application that allows you to track scheduled tasks, as well as assign them statuses and labels for the convenience of staying.

### Implemented:
- User registration and authorization
- Creating statuses and labels
- Creating tasks, as well as assigning statuses and labels to them
- Deleting users, tasks, statuses, and labels
- Error tracking in Rollbar
- Russian and English localizations
- The application works with PostgreSQL databases

## Installation and launch:

### Install:
```
pip install poetry
git clone https://github.com/sat-brr/python-project-52.git
make install
```

#### Environment variables:
Create .env file in the root of the project and specify the variables:
- DEBUG = True/False starting in debug mode or not
- DATABASE_URL = URL to DB in the format postgresql://user:password@server:port/dbname
- SECRET_KEY = Your django secret key
- ROLLBAR_TOKEN: Your rollbar token

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