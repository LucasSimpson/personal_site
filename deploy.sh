#!/bin/bash

# build inline css
# set env debug to False
# zappa update
# set env debug to True

echo "Deploying..."

export DEBUG="False"
python manage.py collectstatic

zappa update
export DEBUG="True"

echo "Done"
