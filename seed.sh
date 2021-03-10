#!/bin/bash

rm -rf budgetapi/migrations
rm db.sqlite3
python3 manage.py migrate
python3 manage.py makemigrations budgetapi
python3 manage.py migrate budgetapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens


# ./seed.sh in the terminal to run the commands.