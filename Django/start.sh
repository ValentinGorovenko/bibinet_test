#!/bin/bash

# Запуск миграций
python manage.py makemigrations
python manage.py migrate

# Загрузка данных
python manage.py load_marks_models
python manage.py load_parts

# Запуск сервера
exec gunicorn --workers=4 --bind=0.0.0.0:8000 bibinet.wsgi:application
