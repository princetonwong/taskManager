# taskManager

## Description
This is a task manager application that allows the user to create, read, update, and delete tasks.

## Table of Contents
* [Technical Information](#technical-information)
* [Quickstart by docker](#quickstart-by-docker)
* [API documentation](#api-documentation)
* [Test by pytest](#unit-test-by-pytest)

## Technical Information
This app mainly uses Python, FastAPI, SQLModel.

For demonstration purpose:

- The PostgreSQL image together with PgAdmin (Database GUI) are also included.
- Secrets are stored in .env file, temporary uploaded here.
- If there is no data in the database, the app will automatically create sample data for you.

User management and authentication is done in combination with API from supabase.com. 

The app is containerized using Docker and docker-compose.


## Quickstart by docker
Run the following command to deploy the application:
```
docker-compose -f docker-compose.yaml up -d
```

## API documentation
Check all available endpoints at

[OpenAPI] http://localhost:8000/docs

[Redoc] http://localhost:8000/redoc

## User management
A simple form is set up to demonstrate user signup and login at
http://localhost:8000/auth/login

## Unit-test by pytest
Run the following command to test the application:
```
docker exec -it taskmanager-backend pytest
```


