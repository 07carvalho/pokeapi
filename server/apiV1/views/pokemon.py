from rest_framework import generics
from rest_framework.response import Response
from apiV1.models.pokemon import Pokemon
from apiV1.serializers.pokemon import PokemonSerializer


class PokemonList(generics.ListAPIView):
    
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
        List pokemons
        """
        serializer = PokemonSerializer(self.get_queryset(), many=True)
        page = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(page)

