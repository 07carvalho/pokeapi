from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from apiV1.models.pokemon import Pokemon
from apiV1.serializers.pokemon import PokemonSerializer


class PokemonList(generics.ListAPIView):
    
    description = 'This route is used to list the Pokemon.'
    serializer_class = PokemonSerializer

    def get_queryset(self):
        """
        Return a Pokemon queryset, if a `q` query parameter
        in the URL, filter Pokemon by name
        """
        queryset = Pokemon.objects.all()
        q = self.request.query_params.get('q', None)
        if q is not None:
            queryset = queryset.filter(name__icontains=q)

        pokemon_type = self.request.query_params.get('type', None)
        if pokemon_type is not None:
            queryset = queryset.filter(types__name=pokemon_type)

        return queryset


    def get(self, request, *args, **kwargs):
        """
        List pokemon
        """
        serializer = PokemonSerializer(self.get_queryset(), many=True)
        page = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(page)


class PokemonDetail(APIView):
    """
    Get a pokemon.
    """

    description = 'This route is used to get a pokemon.'
    permission_classes = ()

    def get_object(self, pokemon_id):
        try:
            obj = Pokemon.objects.get(pk=pokemon_id)
            self.check_object_permissions(self.request, obj)
            return obj
        except Pokemon.DoesNotExist:
            raise serializers.ValidationError({'not_found': _('This Pokemon does not exist.')})


    def get(self, request, pokemon_id, format=None):
        team = self.get_object(pokemon_id)
        serializer = PokemonSerializer(team)
        return Response(serializer.data, status=status.HTTP_200_OK)

