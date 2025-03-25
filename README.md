# drf-demo
The task is to create an application which allows users to authenticate, search for a product and perform simple 
operations with the search result.

The project board is available here: https://github.com/users/bnisevic/projects/2

### Development Env

`docker compose up --build`

This will automatically use Dockerfile.dev

### Production Env

Uses production Dockerfile on Divio. Created superuser for testing purposes:
username: bob
password: change123

### API Documentation available at: http://<host_address:port>/swagger/

## Running Tests on Backend in dev env
 docker compose run backend coverage run manage.py test

## Creating Superuser in dev env
 docker compose run backend python manage.py createsuperuser
