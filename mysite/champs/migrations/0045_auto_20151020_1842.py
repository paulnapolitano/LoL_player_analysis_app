# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('champs', '0044_auto_20151020_1840'),
    ]

    operations = [
        migrations.AlterField(
            model_name='championtag',
            name='tag',
            field=models.CharField(max_length=15, serialize=False, primary_key=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='match',
            name='match_id',
            field=models.CharField(max_length=20, serialize=False, primary_key=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='std_summoner_name',
            field=models.CharField(default=b'UNKNOWN', max_length=20, db_index=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='summoner_id',
            field=models.CharField(max_length=20, serialize=False, primary_key=True, db_index=True),
        ),
    ]
