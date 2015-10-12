# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('champs', '0022_auto_20150904_0619'),
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('matchId', models.CharField(max_length=20, serialize=False, primary_key=True)),
                ('matchDuration', models.IntegerField(default=0)),
                ('matchCreation', models.DateTimeField()),
            ],
        ),
        migrations.RemoveField(
            model_name='statset',
            name='id',
        ),
        migrations.RemoveField(
            model_name='statset',
            name='matchId',
        ),
        migrations.RemoveField(
            model_name='statset',
            name='matchLength',
        ),
        migrations.AddField(
            model_name='statset',
            name='statsetId',
            field=models.CharField(default=b'UNKNOWN', max_length=20, serialize=False, primary_key=True),
        ),
        migrations.AddField(
            model_name='statset',
            name='match',
            field=models.ForeignKey(to='champs.Match', null=True),
        ),
    ]
