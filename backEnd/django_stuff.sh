#!/bin/bash
rm db.sqlite3
rm interestsProfile/temp_algo_index.pkl
find . -path "/migrations/.py" -not -name "init.py" -delete
find . -path "/migrations/.pyc"  -delete
find . -path "/user_profile_pictures/.png"  -delete
python3 manage.py makemigrations authUser profileUser locationUser matchesUser interestsProfile statsUser actionsUser
python3 manage.py migrate
python3 manage.py runserver
