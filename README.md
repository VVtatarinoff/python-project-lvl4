## Hexlet tests and linter status:
[![Actions Status](https://github.com/VVtatarinoff/python-project-lvl4/workflows/hexlet-check/badge.svg)](https://github.com/VVtatarinoff/python-project-lvl4/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/789a4c8d67e882385320/maintainability)](https://codeclimate.com/github/VVtatarinoff/python-project-lvl4/maintainability)
[![Linter-check](https://github.com/VVtatarinoff/python-project-lvl4/actions/workflows/linter.yml/badge.svg)](https://github.com/VVtatarinoff/python-project-lvl4/actions/workflows/linter.yml)
[![Test Coverage](https://api.codeclimate.com/v1/badges/789a4c8d67e882385320/test_coverage)](https://codeclimate.com/github/VVtatarinoff/python-project-lvl4/test_coverage)


Task manager is a tool to help tracking progress and statuses other various tasks.

## Example of website:
[Task manager](https://ancient-gorge-78100.herokuapp.com/)

## Local usage
to install locally you should clone the repository:
##### python3 -m pip install --user git+https://github.com/VVtatarinoff/python-project-lvl4

You could launch the project either in docker or locally:
###### To start locally:
The file ".env" should be created in root directory
You should list there local variables:
    SECRET_KEY='your secret here there'
    ENGINE='django.db.backends.sqlite3' - if you want to use sqlite
    DB_NAME='db.sqlite3'    -name of the database 
    DEBUG=True   - if you want to enter a debug environment
to install dependencies:
    pip install -r requirements.txt

After creation of .env file the migration should be started by two commands:
python manage.py makemigrations
python manage.py migrate

To launch the program:
python manage.py runserver

usually it started at address http://127.0.0.1:8000/
###### To start in docker:
Check the instructions in docker folder


This project was built using these tools:

| Tool                                         | Description                                             |
|----------------------------------------------|---------------------------------------------------------|
| [django](https://www.djangoproject.com/)     | "The web framework for perfectionists with deadlines."  |
| [poetry](https://poetry.eustace.io/)         | "Python dependency management and packaging made easy"  |
| [flake](https://flake8.pycqa.org/en/latest/) | "Tool For Style Guide Enforcement"                      |
| [pytest](https://pytest.org/en/latest/)      | "Helps you write better programs"                       |
| [docker](https://www.docker.com/)            | "Developers Love Docker.Businesses Trust It."   