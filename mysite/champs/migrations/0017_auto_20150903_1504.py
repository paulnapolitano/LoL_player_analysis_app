# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('champs', '0016_auto_20150903_1408'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='champ',
            name='lane_name',
        ),
        migrations.RemoveField(
            model_name='champ',
            name='role_name',
        ),
    ]
