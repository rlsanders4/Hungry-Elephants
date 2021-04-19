#! /bin/bash
python3 ./website/manage.py migrate
python3 ./website/manage.py runserver 0.0.0.0:8001&
python3 ./server_controller/main.py -v
