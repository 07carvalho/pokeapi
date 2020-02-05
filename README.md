# pokeapi
An API to a Pokemon Game

##  Instalation
### Via Docker
For this installation way, we are assuming yout have [Docker-compose](https://docs.docker.com/compose/install/) installed.

#### Step by Step
Go to server folder

    cd server
Copy the .env_example file to .env

    cp .env_example .env

Build the project

    make build
Start the containers

    make up

Create all the tables of the database

    make migration

Populate the database with initial data

    make loaddata

Then, open the browser in [localhost:8000](http://localhost:8000/)

### Manually
For this installation way, we are assuming you have a [Virtualenv](https://virtualenv.pypa.io/en/latest/) actived and the [PostgreSQL](https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-16-04) installed.

#### Step by Step
Go to server folder

    cd server

Install all the necessaries packages:

    pip install -r requirements.txt

Copy the .env_example file to .env

    cp .env_example .env

Create all the tables of the database

    python manage.py migrate

Run this script to populate the database with initial database

    python manage.py loaddata pokemon_load_data.json

Start the server

    python manage.py runserver

Then, open the browser in [localhost:8000](http://localhost:8000/)

## Testing
If you are using Compose, run the tests with

    make test

Otherwise, run

    python manage.py test


