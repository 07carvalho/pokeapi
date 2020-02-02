'''
This script load the PokeAPI database with the Pokemons in docs/pokemon.json
To run just load the enviroment and execute 

python load_data.py

'''

import json
import os
import django
from django.db import transaction
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pokeapi.settings")
django.setup()

from apiV1.models.pokemon import *

with open('../docs/pokemon.json') as json_file:
    data = json.load(json_file)
    for pokemon in data['pokemon']:
        with transaction.atomic():
            print(pokemon)
            _id = pokemon.pop('id')
            types_list = pokemon.pop('types')
            obj = Pokemon.objects.create(**pokemon)

            for tp in types_list:
                t, created = PokemonType.objects.get_or_create(name=tp)
                obj.types.add(t)