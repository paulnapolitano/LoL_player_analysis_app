# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('champs', '0029_player_std_summoner_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='profile_icon_id',
            field=models.CharField(default=b'UNKNOWN', max_length=20, blank=True),
        ),
        migrations.AddField(
            model_name='player',
            name='summoner_level',
            field=models.IntegerField(default=0),
        ),
    ]
