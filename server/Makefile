build:
	docker-compose build

up:
	docker-compose up -d

up-non-daemon:
	docker-compose up

migrate:
	docker-compose run web python3 manage.py migrate

loaddata:
	docker-compose run web python3 manage.py loaddata pokemon_load_data.json

start:
	docker-compose start

stop:
	docker-compose stop

restart:
	docker-compose stop && docker-compose start

test:
	docker-compose run web python3 manage.py test