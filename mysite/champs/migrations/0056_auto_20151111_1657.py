# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('champs', '0055_auto_20151111_1517'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='losses',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='player',
            name='wins',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
