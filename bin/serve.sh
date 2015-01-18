#!/bin/bash

ADDR=${2:-localhost}
PORT=${3:-8000}

echo "Running $SITE server on $ADDR:$PORT .."
source env/bin/activate \
    && python manage.py runserver $ADDR:$PORT
deactivate
