#!/usr/bin/env bash

pip install -r requirementss.txt

python manage.py collectstatic --noinput

python manage.py migrate