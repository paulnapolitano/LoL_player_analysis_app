# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('champs', '0008_statset_summoner_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='statset',
            name='match_version',
            field=models.CharField(default='UNKNOWN', max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='champ',
            name='champ_name',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='champ',
            name='lane_name',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='champ',
            name='league_name',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='champ',
            name='role_name',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='champ',
            name='smart_role_name',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='statset',
            name='match_id',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='statset',
            name='summoner_id',
            field=models.CharField(max_length=20),
        ),
    ]
