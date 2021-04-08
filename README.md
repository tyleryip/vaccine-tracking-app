# Vaccine Tracking App

A vaccine tracking app, designed and implemented for our CPSC 471 - Database Management Systems course project.

## Installation

Ensure that you have a Django-compatible version of Python installed on your machine. Django 3.0 currently supports Python 3.6, 3.7, 3.8, and 3.9. For more information on Django-Python compatibility, see [Django compatibility](https://docs.djangoproject.com/en/3.1/releases/3.0/)

Use pip to install the required dependencies for this project.

```bash
pip install -r requirements.txt
```

## Usage

Django's base manage.py utility tool provides some built in command line commands to interact with the project. These commands must be run from the cpsc471-project directory.

To run the development server, run the following command:
```bash
python manage.py runserver
```

Our project ships with some sample data in a csv file. To load this data, run the following command:
```bash
python manage.py populate_db sampledata3.csv
```

To clear the database of all application data (models excluding admin/authentication data), run the following command:
```bash
python manage.py clear_db
```