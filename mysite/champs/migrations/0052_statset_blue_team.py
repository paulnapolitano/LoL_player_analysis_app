# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('champs', '0051_auto_20151028_2145'),
    ]

    operations = [
        migrations.AddField(
            model_name='statset',
            name='blue_team',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
