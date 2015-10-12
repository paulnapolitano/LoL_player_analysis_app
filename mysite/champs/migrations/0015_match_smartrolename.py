# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('champs', '0014_remove_match_smartrolename'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='smartRoleName',
            field=models.CharField(default='UNKNOWN', max_length=20),
            preserve_default=False,
        ),
    ]
