# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('champs', '0054_auto_20151111_1434'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='last_revision',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='profile_icon_id',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='summoner_level',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
