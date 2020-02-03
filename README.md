# pokeapi
An API to a Pokemon Game

###  Prerequisites
 - [Virtualenv](https://virtualenv.pypa.io/en/latest/) 

### Instalation
Go to server folder

    cd server

Install all the necessaries packages:

    pip install -r requirements.txt

Create all the tables of the database

    python manage.py migrate

Run this script to populate the database

    python load_data.py

Start the server

    python manage.py runserver


### Testing
To test the application, run

    python manage.py test

