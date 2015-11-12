# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('champs', '0053_auto_20151109_0004'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='division',
            field=models.CharField(default=b'UNKNOWN', max_length=3),
        ),
        migrations.AddField(
            model_name='player',
            name='lp',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='player',
            name='tier',
            field=models.CharField(default=b'UNKNOWN', max_length=10),
        ),
    ]
