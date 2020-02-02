from rest_framework import serializers
from apiV1.models.pokemon import PokemonType


class PokemonTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = PokemonType
        fields = '__all__'

