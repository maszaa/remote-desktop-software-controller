#!/bin/bash

cd ../

git pull origin master

source virtualenv/Scripts/activate
pip install -r dev.requirements.txt
pip install -r requirements.txt

cd app

while True
do
    python manage.py runserver 0.0.0.0:80
    sleep 1
done
