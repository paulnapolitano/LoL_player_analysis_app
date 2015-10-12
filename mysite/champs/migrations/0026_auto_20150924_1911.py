# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('champs', '0025_player_summoner_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='last_update',
            field=models.DateTimeField(default=django.utils.timezone.now, blank=True),
        ),
    ]
