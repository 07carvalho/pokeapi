from django.contrib.auth.models import User
from django.db import models
from apiV1.models.pokemon import Pokemon


class Team(models.Model):
    '''
    This model represents a Pokemon team, with a trainer and many pokemon
    '''

    class Meta:
        app_label = 'apiV1'

    name = models.CharField(max_length=64)
    trainer = models.ForeignKey(User, on_delete=models.CASCADE)
    pokemons = models.ManyToManyField('Pokemon')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return '{0}, trained by @{1}'.format(self.name, self.trainer.username)

