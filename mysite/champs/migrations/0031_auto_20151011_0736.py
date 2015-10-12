# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('champs', '0030_auto_20150926_1625'),
    ]

    operations = [
        migrations.CreateModel(
            name='BuildComponent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('item_birth', models.IntegerField()),
                ('item_death', models.IntegerField()),
                ('item_batch', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('depth', models.IntegerField(blank=True)),
                ('description', models.CharField(max_length=5000, blank=True)),
                ('group', models.CharField(max_length=30, blank=True)),
                ('name', models.CharField(max_length=30, blank=True)),
                ('map_1', models.BooleanField(default=False)),
                ('map_8', models.BooleanField(default=False)),
                ('map_10', models.BooleanField(default=False)),
                ('map_11', models.BooleanField(default=False)),
                ('map_12', models.BooleanField(default=False)),
                ('map_14', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ItemParentChild',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('child_id', models.ForeignKey(related_name='child', to='champs.Item')),
                ('parent_id', models.ForeignKey(related_name='parent', to='champs.Item')),
            ],
        ),
        migrations.AddField(
            model_name='buildcomponent',
            name='item',
            field=models.ForeignKey(to='champs.Item', blank=True),
        ),
        migrations.AddField(
            model_name='buildcomponent',
            name='statset',
            field=models.ForeignKey(to='champs.StatSet', blank=True),
        ),
    ]
