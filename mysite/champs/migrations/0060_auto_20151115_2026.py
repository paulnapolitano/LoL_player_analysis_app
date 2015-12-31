# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('champs', '0059_auto_20151115_2023'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='version',
            name='end_datetime',
        ),
        migrations.RemoveField(
            model_name='version',
            name='start_datetime',
        ),
        migrations.AddField(
            model_name='version',
            name='current',
            field=models.BooleanField(default=False),
        ),
    ]
