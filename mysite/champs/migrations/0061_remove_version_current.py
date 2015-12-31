# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('champs', '0060_auto_20151115_2026'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='version',
            name='current',
        ),
    ]
