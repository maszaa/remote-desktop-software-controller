#!/bin/bash

cd ../

git pull origin master

source virtualenv/Scripts/activate
pip install -r dev.requirements.txt
pip install -r requirements.txt

cd app

SECRET_KEY="secretkey.txt"
test -f $SECRET_KEY || python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())" > $SECRET_KEY

winpty python manage.py migrate --noinput

while True
do
    winpty python manage.py runserver 0.0.0.0:80
    sleep 1
done
