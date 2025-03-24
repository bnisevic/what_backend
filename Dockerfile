# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the prod.env file to .env
COPY what_backend/prod.env what_backend/.env

# Copy the current directory contents into the container at /app
RUN mkdir -p /app/db && chmod -R 755 /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

RUN python manage.py collectstatic --noinput
RUN python manage.py migrate
RUN python manage.py loaddata api/fixtures/products.json
RUN python manage.py test

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run gunicorn when the container launches
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "what_backend.wsgi:application"]