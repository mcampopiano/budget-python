#!/bin/bash

rm -rf budgetapi/migrations
rm db.sqlite3
python3 manage.py migrate
python3 manage.py makemigrations budgetapi
python3 manage.py migrate budgetapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens
python3 manage.py loaddata budgets
python3 manage.py loaddata envelopes
python3 manage.py loaddata generalExpenses
python3 manage.py loaddata deposits
python3 manage.py loaddata recurringBills
python3 manage.py loaddata payments


# ./seed.sh in the terminal to run the commands.