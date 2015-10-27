# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('champs', '0046_auto_20151023_1936'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemStatic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('item_id', models.CharField(db_index=True, max_length=4, blank=True)),
                ('img', models.CharField(max_length=50, blank=True)),
                ('version', models.CharField(db_index=True, max_length=50, blank=True)),
                ('depth', models.IntegerField(blank=True)),
                ('description', models.CharField(max_length=5000, blank=True)),
                ('name', models.CharField(max_length=30, blank=True)),
                ('gold_purchasable', models.BooleanField(default=False)),
                ('gold_base', models.IntegerField(null=True, blank=True)),
                ('gold_sell', models.IntegerField(null=True, blank=True)),
                ('gold_total', models.IntegerField(null=True, blank=True)),
                ('map_1', models.BooleanField(default=False)),
                ('map_8', models.BooleanField(default=False)),
                ('map_10', models.BooleanField(default=False)),
                ('map_11', models.BooleanField(default=False)),
                ('map_12', models.BooleanField(default=False)),
                ('map_14', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='championstatic',
            name='img',
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AddField(
            model_name='championstatic',
            name='version',
            field=models.CharField(db_index=True, max_length=50, blank=True),
        ),
        migrations.AlterField(
            model_name='buildcomponent',
            name='item',
            field=models.ForeignKey(to='champs.ItemStatic', blank=True),
        ),
        migrations.AlterField(
            model_name='itemparentchild',
            name='child_id',
            field=models.ForeignKey(related_name='child', to='champs.ItemStatic'),
        ),
        migrations.AlterField(
            model_name='itemparentchild',
            name='parent_id',
            field=models.ForeignKey(related_name='parent', to='champs.ItemStatic'),
        ),
        migrations.DeleteModel(
            name='Item',
        ),
    ]
