#!/bin/sh

# Run the server in the background
python manage.py runserver 0.0.0.0:8000 &

# Wait for the server to start
sleep 5

# Run migrations and load data
python manage.py migrate
python manage.py loaddata api/fixtures/products.json

# Keep the container running
tail -f /dev/null
