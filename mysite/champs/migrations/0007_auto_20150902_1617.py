# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('champs', '0006_auto_20150902_0518'),
    ]

    operations = [
        migrations.AddField(
            model_name='champ',
            name='lane_name',
            field=models.CharField(default='UNKNOWN', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='champ',
            name='role_name',
            field=models.CharField(default='UNKNOWN', max_length=200),
            preserve_default=False,
        ),
    ]
