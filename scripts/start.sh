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
winpty python manage.py collectstatic --noinput

while True
do
    winpty python manage.py start 0.0.0.0 80 $(( $NUMBER_OF_PROCESSORS * 2 ))
    sleep 1
done
