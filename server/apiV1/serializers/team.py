from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from apiV1.models.team import Team
from apiV1.serializers.pokemon import PokemonSerializer


class TeamSerializer(serializers.ModelSerializer):
    """
    This serializer will reaturn a teams list trained by an user.
    This serializer will operate for GET requests.
    """
    pokemons = PokemonSerializer(many=True)
    created_at = serializers.SerializerMethodField()


    def get_created_at(self, obj):
        return obj.created_at.strftime("%m/%d/%Y %H:%M:%S")


    class Meta:
        model = Team
        # excludind the trainer field from the serializer, once the request
        # will return only teams trained by the user
        exclude = ('trainer', )


class TeamRegistrationSerializer(serializers.ModelSerializer):
    """
    This serializer will validade the registration and update of a team.
    With this specific serializer for POST and PUT requests, we are able to work with
    a different data format, avoiding the overhead of pass a list of Pokemon Dicts as parameter  
    """
    pokemons = serializers.ListField()


    class Meta:
        model = Team
        # excludind the trainer field from the serializer, once the request
        # will return only teams treined by the user
        exclude = ('trainer', )


    min_characters_qty = 5
    min_pokemon_qty = 1
    max_pokemon_qty = 6
    default_error_messages = {
        'invalid_name': ('The team name must have at least {} characters.').format(min_characters_qty),
        'invalid_pokemon_quantity': ('The team must have between {} and {} pokemon.').format(min_pokemon_qty, max_pokemon_qty),
    }

    def validate(self, data):
        """
        Verify if the team name has more at least characters and
        has between one and six pokemon
        """
        name = data.get('name')
        pokemons = data.get('pokemons')
        errors = []
        if len(name) < self.min_characters_qty:
            errors.append({'invalid_name': _(self.error_messages['invalid_name'])})
        
        if len(pokemons) < self.min_pokemon_qty or len(pokemons) > self.max_pokemon_qty:
            errors.append({'invalid_pokemon_quantity': _(self.error_messages['invalid_pokemon_quantity'])})

        if len(errors) > 0:
            raise serializers.ValidationError(errors)
        return data

