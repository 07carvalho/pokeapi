from rest_framework import serializers
from apiV1.models.pokemon import Pokemon
from apiV1.serializers.pokemon_type import PokemonTypeSerializer


class PokemonSerializer(serializers.ModelSerializer):

    types = PokemonTypeSerializer(many=True)

    class Meta:
        model = Pokemon
        fields = '__all__'

