import json
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from apiV1.models.pokemon import *


class PokemonModelTest(TestCase):

    def create_pokemon(self, data):
        types_list = data.pop('types')
        obj = Pokemon.objects.create(**data)

        for tp in types_list:
            t, created = PokemonType.objects.get_or_create(name=tp)
            obj.types.add(t)

        return obj


    def test_pokemon_creation(self):
        data = {
            'name': 'bulbasaur',
            'height': 0.7,
            'weight': 6.9,
            'xp': 64,
            'types': ['poison', 'grass'],
            'image': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png'
        }

        p = self.create_pokemon(data)
        self.assertTrue(isinstance(p, Pokemon))
        self.assertEqual(p.__str__(), p.name)
        self.assertEqual(2, p.types.count())


class PokemonListAPIViewTestCase(APITestCase):

    url = reverse('pokemon_list')

    def setUp(self):
        data = {
            'name': 'bulbasaur',
            'height': 0.7,
            'weight': 6.9,
            'xp': 64,
            'types': ['poison', 'grass'],
            'image': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png'
        }

        types_list = data.pop('types')
        self.pokemon = Pokemon.objects.create(**data)

        for tp in types_list:
            t, created = PokemonType.objects.get_or_create(name=tp)
            self.pokemon.types.add(t)


    def test_list_pokemon(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)


    def test_filter_pokemon_by_name(self):
        response = self.client.get(self.url, {'q': 'bulb'})
        self.assertEqual(200, response.status_code)


    def test_filter_pokemon_by_name_and_get_empty(self):
        response = self.client.get(self.url, {'q': 'zzz'})
        self.assertEqual(0, len(response.data.get('results')))


    def test_filter_pokemon_by_type(self):
        response = self.client.get(self.url, {'type': 'poison'})
        self.assertEqual(200, response.status_code)


    def test_filter_pokemon_by_type_and_get_empty(self):
        response = self.client.get(self.url, {'type': 'chocolate'})
        self.assertEqual(0, len(response.data.get('results')))


    def test_filter_pokemon_by_name_and_type(self):
        response = self.client.get(self.url, {'q': 'bulb', 'type': 'poison'})
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.data.get('results')))


class UserRegistrationAPIViewTestCase(APITestCase):

    url = reverse('user_registration')

    def test_registration_user(self):
        data = {
            'username': 'ash',
            'email': 'ash@gmail.com',
            'password': 'pikachu',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(201, response.status_code)
        self.assertTrue('auth_token' in json.loads(response.content))


    def test_email_validation(self):
        """
        Try to create two users with the same email
        """
        data1 = {
            'username': 'misty',
            'email': 'misty@gmail.com',
            'password': 'admin',
        }
        response = self.client.post(self.url, data1)
        self.assertEqual(201, response.status_code)

        data2 = {
            'username': 'jessie',
            'email': 'misty@gmail.com',
            'password': '123456',
        }
        response = self.client.post(self.url, data2)
        self.assertEqual(400, response.status_code)


class UserLoginAPIViewTestCase(APITestCase):

    url = reverse('user_login')

    def setUp(self):
        self.user = User.objects.create_user('ash', 'ash@gmail.com', 'pikachu')
        

    def test_login_right_credentials(self):
        data = {
            'username': 'ash',
            'password': 'pikachu',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(200, response.status_code)
        self.assertTrue('auth_token' in json.loads(response.content))


    def test_login_wrong_credentials(self):
        # trying to login with the wrong password
        data1 = {
            'username': 'ash',
            'password': 'p123',
        }
        response = self.client.post(self.url, data1)
        self.assertEqual(400, response.status_code)

        # trying to login with the wrong username
        data2 = {
            'username': 'ash2',
            'password': 'pikachu',
        }
        response = self.client.post(self.url, data2)
        self.assertEqual(400, response.status_code)


class TeamAPIViewTestCase(APITestCase):

    login_url = reverse('user_login')
    team_list_url = reverse('team_list')
    team_detail_url = None

    def setUp(self):
        # create user
        self.user = User.objects.create_user('ash', 'ash@gmail.com', 'pikachu')

        # login
        data = {
            'username': 'ash',
            'password': 'pikachu',
        }
        response = self.client.post(self.login_url, data)

        self.auth_token = json.loads(response.content).get('auth_token')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.auth_token)

        # create seven pokemon
        for i in range(0, 8):
            data = {
                'name': 'bulbasaur' + str(i),
                'height': 0.7,
                'weight': 6.9,
                'xp': 64,
                'types': ['poison', 'grass'],
                'image': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png'
            }

            types_list = data.pop('types')
            pokemon = Pokemon.objects.create(**data)

            for tp in types_list:
                t, created = PokemonType.objects.get_or_create(name=tp)
                pokemon.types.add(t)


    def test_registration_team_wrong_name(self):
        data = {
            "name": "Poke",
            "pokemons": [1,2,3,4,5]
        }
        response = self.client.post(self.team_list_url, data, format='json' )
        self.assertEqual(400, response.status_code)


    def test_registration_team_wrong_pokemon_qty(self):
        data = {
            "name": "Gotta catch 'em all!",
            "pokemons": []
        }
        response = self.client.post(self.team_list_url, data, format='json' )
        self.assertEqual(400, response.status_code)

        data = {
            "name": "Gotta catch 'em all!",
            "pokemons": [1,2,3,4,5,6,7]
        }
        response = self.client.post(self.team_list_url, data, format='json' )
        self.assertEqual(400, response.status_code)


    def test_registration_and_update_team(self):
        # registration
        data = {
            "name": "Gotta catch 'em all!",
            "pokemons": [1,2,3,4,5]
        }
        response = self.client.post(self.team_list_url, data, format='json' )
        self.assertEqual(201, response.status_code)
        self.assertEqual(len(data.get('pokemons')), len(json.loads(response.content).get('pokemons')))
        self.team_detail_url = reverse('team_detail', kwargs={'team_id': json.loads(response.content).get('id')})

        # update
        new_data = {
            "name": "Gotta catch 'em all!",
            "pokemons": [3,4,5]
        }
        response = self.client.put(self.team_detail_url, new_data, format='json' )
        self.assertEqual(200, response.status_code)
        self.assertEqual(len(new_data.get('pokemons')), len(json.loads(response.content).get('pokemons')))


        