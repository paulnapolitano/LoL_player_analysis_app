# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('champs', '0017_auto_20150903_1504'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='champ',
            name='id',
        ),
        migrations.AddField(
            model_name='champ',
            name='champ_pk',
            field=models.CharField(default=b'UNKNOWN', max_length=30, serialize=False, primary_key=True),
        ),
    ]
