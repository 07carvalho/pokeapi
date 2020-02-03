from django.urls import path

from apiV1.views import pokemon, user

urlpatterns = [
    path('pokemons/', pokemon.PokemonList.as_view(), name='pokemon_list'),
    path('users/', user.UserRegistration.as_view(), name='user_registration'),
    path('login/', user.UserLogin.as_view(), name='user_login'),
    path('logout/', user.UserLogout.as_view(), name='user_logout'),
]
