# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('champs', '0002_auto_20150830_0525'),
    ]

    operations = [
        migrations.RenameField(
            model_name='statset',
            old_name='game_id',
            new_name='match_id',
        ),
        migrations.AddField(
            model_name='champ',
            name='champ_id',
            field=models.IntegerField(default=25),
            preserve_default=False,
        ),
    ]
