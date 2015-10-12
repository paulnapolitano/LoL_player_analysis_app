# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('champs', '0003_auto_20150831_1531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='champ',
            name='lane_name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='champ',
            name='league_name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='champ',
            name='role_name',
            field=models.CharField(max_length=200),
        ),
    ]
