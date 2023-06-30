# taskManager

## Description
This is a task manager application that allows the user to create, read, update, and delete tasks.

## Table of Contents
* [Technical Information](#technical-information)
* [Quickstart by docker](#quickstart-by-docker)
* [Test by pytest](#test-by-pytest)

## Technical Information
This app uses FastAPI, SQLModel, Pydantic, SQLAlchemy.

The PostgreSQL image together with PgAdmin is pulled from dockerhub.

Secrets are stored in .env file.

Authentication is done in connection to API from supabase.com.

The app is containerized using Docker and docker-compose.

It is tested using pytest.

## Quickstart by docker
Run the following command to deploy the application:
```
docker-compose -f docker-compose.yaml up -d
```

## See the API documentation
Go to http://localhost:8000/docs
or http://localhost:8000/redoc

## User management
A simple form is set up to demonstrate user signup and login at
http://localhost:8000/auth/login

## Unit-test by pytest
Run the following command to test the application:
```
docker exec -it taskmanager-backend pytest
```

If there is no data in the database, the app will automatically create sample data for you.


