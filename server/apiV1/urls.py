from django.urls import path

from apiV1.views import pokemon, team, user

urlpatterns = [
    path('login/', user.UserLogin.as_view(), name='user_login'),
    path('logout/', user.UserLogout.as_view(), name='user_logout'),
    path('pokemons/', pokemon.PokemonList.as_view(), name='pokemon_list'),
    path('teams/', team.TeamList.as_view(), name='team_list'),
    path('teams/<int:team_id>/', team.TeamDetail.as_view(), name='team_detail'),
    path('users/', user.UserRegistration.as_view(), name='user_registration'),
]
