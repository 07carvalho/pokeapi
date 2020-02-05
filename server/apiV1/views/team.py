from django.db import transaction
from django.utils.translation import ugettext_lazy as _
from rest_framework import generics, serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from apiV1.models.pokemon import Pokemon
from apiV1.models.team import Team
from apiV1.permissions import IsTrainer
from apiV1.serializers.team import TeamSerializer, TeamRegistrationSerializer


class TeamList(generics.ListCreateAPIView):

    description = 'This route is used to list the teams of a user or create a new team.'
    permission_classes = (IsTrainer,)
    serializer_class = TeamRegistrationSerializer

    def get_queryset(self):
        """
        Return a Team queryset filtered by trainer
        """
        return Team.objects.filter(trainer=self.request.user)


    def get(self, request, *args, **kwargs):
        """
        List Pokemon teams
        """
        serializer = TeamSerializer(self.get_queryset(), many=True)
        page = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(page)


    def create(self, request, *args, **kwargs):
        """
        Create a Pokemon team
        """
        serializer = TeamRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = request.data
        pokemons = validated_data.pop('pokemons')

        with transaction.atomic():
            team = Team.objects.create(**validated_data, trainer=request.user)
            for pokemon_id in pokemons:
                try:
                    pokemon = Pokemon.objects.get(pk=pokemon_id)
                    team.pokemons.add(pokemon)
                except Exception as e:
                    raise serializers.ValidationError({'invalid_pokemon': _('You chose a pokemon that doesn\'t exist. Failed to create your team.')})

        serializer = TeamSerializer(team)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TeamDetail(APIView):
    """
    Get, update or delete a pokemon team.
    """

    description = 'This route is used to get, update or delete a team of a user.'
    permission_classes = (IsTrainer,)

    def get_object(self, team_id):
        try:
            obj = Team.objects.get(pk=team_id)
            self.check_object_permissions(self.request, obj)
            return obj
        except Team.DoesNotExist:
            raise serializers.ValidationError({'not_found': _('This team does not exist.')})


    def get(self, request, team_id, format=None):
        team = self.get_object(team_id)
        serializer = TeamSerializer(team)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def put(self, request, team_id, format=None):
        serializer = TeamRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        team = self.get_object(team_id)
        with transaction.atomic():
            team.name = request.data.get('name', team.name)
            team.save()

            # remove all pokemons from team
            team.pokemons.clear()

            # add the pokemons from list to team
            pokemons = request.data.pop('pokemons')
            for pokemon_id in pokemons:
                try:
                    pokemon = Pokemon.objects.get(pk=pokemon_id)
                    team.pokemons.add(pokemon)
                except Exception as e:
                    raise serializers.ValidationError({'invalid_pokemon': _('You chose a pokemon that doesn\'t exist. Failed to create your team.')})

            serializer = TeamSerializer(team)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def delete(self, request, team_id, format=None):
        team = self.get_object(team_id)
        with transaction.atomic():
            team.delete()
            return Response(status=status.HTTP_204_NO_CONTENT) 
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

