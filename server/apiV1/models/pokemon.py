from django.db import models


class Pokemon(models.Model):
    '''
    This model represents a pokemon. As a pokemon has one or two types,
    a many-to-many relationship was created to persist the pokemon type
    '''

    class Meta:
        app_label = 'apiV1'

    name = models.CharField(max_length=64)
    height = models.FloatField()
    weight = models.FloatField()
    xp = models.IntegerField()
    types = models.ManyToManyField('PokemonType')
    image = models.URLField()

    def __str__(self):
        return self.name


class PokemonType(models.Model):
    '''
    This model represents a pokemon type. As the name of a type is unique
    and there are only 18 types, the name will be used as primary key
    '''

    class Meta:
        app_label = 'apiV1'

    name = models.CharField(primary_key=True, max_length=64)

    def __str__(self):
        return '{0}'.format(self.name)

