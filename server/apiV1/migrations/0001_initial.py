# Generated by Django 3.0.2 on 2020-01-31 03:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PokemonType',
            fields=[
                ('name', models.CharField(max_length=64, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Pokemon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('height', models.FloatField()),
                ('weight', models.FloatField()),
                ('xp', models.IntegerField()),
                ('image', models.URLField()),
                ('types', models.ManyToManyField(to='apiV1.PokemonType')),
            ],
        ),
    ]
