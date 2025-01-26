@echo off

:: Set user details
set DJANGO_USER_EMAIL=test@test.com
set DJANGO_USER_PASSWORD=test
set DJANGO_USER_USERNAME=test

:: Use Django shell to create a normal user
echo Creating normal user...
py manage.py createsuperuser --email="%DJANGO_USER_EMAIL%" --noinput

echo Normal user created with username %DJANGO_USER_USERNAME% and email %DJANGO_USER_EMAIL%