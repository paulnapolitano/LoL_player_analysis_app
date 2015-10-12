# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('champs', '0028_auto_20150924_2114'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='std_summoner_name',
            field=models.CharField(default=b'UNKNOWN', max_length=20),
        ),
    ]
