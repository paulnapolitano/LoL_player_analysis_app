# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('champs', '0049_auto_20151026_2024'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='champ',
            name='champ_id',
        ),
        migrations.RemoveField(
            model_name='champ',
            name='champ_name',
        ),
        migrations.RemoveField(
            model_name='championstatic',
            name='tags',
        ),
        migrations.AddField(
            model_name='champ',
            name='champion',
            field=models.ForeignKey(blank=True, to='champs.ChampionStatic', null=True),
        ),
    ]
