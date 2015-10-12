# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('champs', '0024_itemset'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='summoner_name',
            field=models.CharField(default=b'UNKNOWN', max_length=20),
        ),
    ]
