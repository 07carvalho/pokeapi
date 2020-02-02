from django.urls import path

from apiV1.views import pokemon

urlpatterns = [
    path('pokemons/', pokemon.PokemonList.as_view(), name='pokemon_list')
]
