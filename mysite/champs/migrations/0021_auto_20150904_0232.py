# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('champs', '0020_auto_20150903_2127'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='rank',
        ),
        migrations.RemoveField(
            model_name='statset',
            name='summonerId',
        ),
        migrations.AddField(
            model_name='player',
            name='last_update',
            field=models.DateField(default=datetime.datetime(2015, 9, 4, 6, 32, 15, 499000, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='player',
            name='rank_num',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='statset',
            name='player',
            field=models.ForeignKey(to='champs.Player', null=True),
        ),
    ]
