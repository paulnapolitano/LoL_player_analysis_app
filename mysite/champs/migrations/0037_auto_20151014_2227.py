# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('champs', '0036_auto_20151014_2030'),
    ]

    operations = [
        migrations.AddField(
            model_name='buildcomponent',
            name='item_birth_time',
            field=models.CharField(max_length=20, blank=True),
        ),
        migrations.AddField(
            model_name='buildcomponent',
            name='item_death_time',
            field=models.CharField(max_length=20, blank=True),
        ),
    ]
