# pokeapi
An API to a Pokemon Game
### About
In this project, I'm using Python 3.6, Django 3 and PostgreSQL. The first commits were with SQLite that already starts with Django, to avoid overhead and speed up the development and delivery of features. In the end, Django's robust ORM allowed me to set PostgreSQL without any problems. I also use the Django Rest Framework (DRF), a powerful library for building APIs that allows high productivity. In the authentication part, I used Auth Token, as recommended by the DRF. To focus on the functionalities first, I left the Docker Compose implementation for last. During the development, I used the branch dev in GitHub, making a pull to the master at the end. To validate the project, I recommend using the browser. I hope you like the result presented. I am available for any questions.

In this document, we will talk about:

 - API Routes
 - Installation
 - Test

## API Routes
#### User Registration

Register a new user.

| Field | Description  |
|--|--|
| URL | [/api/v1/users/](http://localhost:8000/api/v1/users/) |
| Method | `POST` |
| URL Params | **Required** <br> None <br><br> **Optional** <br> None |
| Data Params | `{username: [string], email: [string], password: [string]}` <br><br> **Example** <br> `{username: "ash", email: "ash@gmail.com", password: "pikachu"}` |
| Samples Call | `curl -d '{username: "ash", email: "ash@gmail.com", password: "pikachu"}' --request POST 'http://localhost:8000/api/v1/users/'` |

---

#### User Login

Log a user in.

| Field | Description |
|--|--|
| URL | [/api/v1/login/](http://localhost:8000/api/v1/login/) |
| Method | `POST` |
| URL Params | **Required** <br> None <br><br> **Optional** <br> None |
| Data Params | `{username: [string], password: [string]}` <br><br> **Example** <br> `{username: "ash", password: "pikachu"}` |
| Samples Call | `curl -d '{username: "ash", password: "pikachu"}' --request POST 'http://localhost:8000/api/v1/login/'` |

---

#### User Logout

Log a user out. Return a Token to use in head requests.

| Field | Description  |
|--|--|
| URL | [/api/v1/logout/](http://localhost:8000/api/v1/logout/) |
| Method | `POST` |
| URL Params | **Required** <br> None <br><br> **Optional** <br> None |
| Data Params | None |
| Samples Call | `curl --request POST 'http://localhost:8000/api/v1/logout/'` |
---

#### Pokemon List

Returns json data about a pokemon list.

| Field | Description  |
|--|--|
| URL | [/api/v1/pokemon/](http://localhost:8000/api/v1/pokemon/) |
| Method | `GET` |
| URL Params | **Required** <br> None <br><br> **Optional** <br>`q=[string]` <br>`type=[string]` <br><br> **Example** <br> `/api/v1/pokemon/?q=bulb`|
| Data Params | None |
| Samples Call | `curl --request GET 'http://localhost:8000/api/v1/pokemon/'` |

---

#### Pokemon Detail

Returns json data about a single Pokemon.

| Field | Description  |
|--|--|
| URL | [/api/v1/pokemon/:id/](http://localhost:8000/api/v1/pokemon/1/) |
| Method | `GET` |
| URL Params | **Required** <br> `id=[integer]` <br><br> **Optional** <br> None <br><br> **Example** <br> `/api/v1/pokemon/1/`|
| Data Params | None |
| Samples Call | `curl --request GET 'http://localhost:8000/api/v1/pokemon/1/'` |

---

#### Team List and Create

Returns json data about a teams list of the user.

| Field | Description  |
|--|--|
| URL | [/api/v1/teams/](http://localhost:8000/api/v1/teams/) |
| Method | `GET|POST` |
| URL Params | **Required** <br> None <br><br> **Optional** <br> None |
| Data Params | **For POST requests** <br> `{name: [string], pokemon: [list]}` <br><br> **Example** <br> `{name: "The Greatest", pokemons: [1,2,3,4,5]}` |
| Samples Call | `curl -H 'Authorization: Token [token]' -H "Content-type: application/json" -d '{"name":"one name","pokemons":[1,2,3,4,5]}' --request POST 'http://localhost:8000/api/v1/teams/'` |

---

#### Team Detail

Returns json data about a single Team.

| Field | Description  |
|--|--|
| URL | [/api/v1/teams/:id/](http://localhost:8000/api/v1/teams/1/) |
| Method | `GET|PUT|DELETE` |
| URL Params | **Required** <br> `id=[integer]` <br><br> **Optional** <br> None <br><br> **Example** <br> `/api/v1/teams/1/` |
| Data Params | **For PUT requests** <br> `{name: [string], pokemon: [list]}` <br><br> **Example** <br> `{name: "The Great One", pokemons: [6,7,8,9,10]}` |
| Samples Call | `curl -H 'Authorization: Token [:token]' -H "Content-type: application/json" -d '{"name":"new name","pokemons":[71,72,73]}' --request PUT 'http://localhost:8000/api/v1/teams/1/'` |

---


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


