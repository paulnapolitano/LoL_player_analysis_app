# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('champs', '0063_player_region'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statset',
            name='blue_team',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='statset',
            name='first_blood_assist',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='statset',
            name='first_blood_kill',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='statset',
            name='first_inhibitor_assist',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='statset',
            name='first_inhibitor_kill',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='statset',
            name='first_tower_assist',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='statset',
            name='first_tower_kill',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='statset',
            name='winner',
            field=models.BooleanField(default=False),
        ),
    ]
