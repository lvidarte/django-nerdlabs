#!/bin/bash

ADDR=${1:-localhost}
PORT=${2:-8000}

echo "Running server on $ADDR:$PORT .."
source env/bin/activate \
    && python manage.py runserver $ADDR:$PORT
deactivate
