# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('champs', '0005_champ_smart_role_name'),
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
