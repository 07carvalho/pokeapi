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

