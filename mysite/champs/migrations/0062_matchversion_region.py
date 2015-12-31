# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('champs', '0061_remove_version_current'),
    ]

    operations = [
        migrations.AddField(
            model_name='matchversion',
            name='region',
            field=models.CharField(max_length=20, blank=True),
        ),
    ]
