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

# Copy the entrypoint script
COPY prod_entrypoint.sh /prod_entrypoint.sh
RUN chmod +x /prod_entrypoint.sh

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Use the entrypoint script
ENTRYPOINT ["/prod_entrypoint.sh"]
