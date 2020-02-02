from django.contrib import admin

from apiV1.models import *

@admin.register(Pokemon, PokemonType)

class ApiV1Admin(admin.ModelAdmin):
    pass