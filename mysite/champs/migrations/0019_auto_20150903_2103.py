# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('champs', '0018_auto_20150903_1853'),
    ]

    operations = [
        migrations.AddField(
            model_name='champ',
            name='match_version',
            field=models.CharField(default=b'UNKNOWN', max_length=20),
        ),
        migrations.AddField(
            model_name='statset',
            name='matchLength',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
