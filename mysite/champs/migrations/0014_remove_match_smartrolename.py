# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('champs', '0013_auto_20150903_0105'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='match',
            name='smartRoleName',
        ),
    ]
