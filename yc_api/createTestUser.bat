@echo off

:: Set user details
set DJANGO_USER_EMAIL=test@test.com
set DJANGO_USER_PASSWORD=test
set DJANGO_USER_USERNAME=test

:: Create a normal user using Django shell
echo Creating normal user...

echo from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_user(username="%DJANGO_USER_USERNAME%", email="%DJANGO_USER_EMAIL%", password="%DJANGO_USER_PASSWORD%") | py manage.py shell

echo Normal user created with username %DJANGO_USER_USERNAME% and email %DJANGO_USER_EMAIL%
