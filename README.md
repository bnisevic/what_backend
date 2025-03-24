# drf-react-demo
The task is to create an application which allows users to authenticate, search for a product and perform simple 
operations with the search result.

The project board is available here: https://github.com/users/bnisevic/projects/2

### Development Env

`docker compose up --build`

This will automatically use:

- docker-compose.yml ✅ (base)
- docker-compose.override.yml ✅ (dev-specific: volume mounts, runserver, hot reload)

🔁 Hot reload is enabled for Django and React through volume mounting and dev servers.


### Production Env

`docker compose -f docker-compose.yml -f docker-compose.prod.yml up --build`

This will:
- Use production Dockerfiles for frontend and backend 
- Run gunicorn for Django 
- Build React static assets with npm run build and serve them with npx serve 
- Avoid mounting your local source code


### API Documentation available at: http://<host_address:port>/swagger/

## Running Tests on Backend
 docker compose run backend coverage run manage.py test

## Creating Superuser
 docker compose run backend python manage.py createsuperuser
