# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('champs', '0007_auto_20150902_1617'),
    ]

    operations = [
        migrations.AddField(
            model_name='statset',
            name='summoner_id',
            field=models.CharField(default='UNKNOWN', max_length=200),
            preserve_default=False,
        ),
    ]
