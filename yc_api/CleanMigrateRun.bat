@echo off
echo Running Django Commands...

py cleanerFiles.py
py manage.py makemigrations
py manage.py migrate

:: Create superuser
set DJANGO_SUPERUSER_EMAIL=admin@admin.com
set DJANGO_SUPERUSER_PASSWORD=admin
set DJANGO_SUPERUSER_USERNAME=admin
py manage.py createsuperuser --noinput

py manage.py runserver

pause
