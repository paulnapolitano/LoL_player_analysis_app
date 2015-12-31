# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('champs', '0052_statset_blue_team'),
    ]

    operations = [
        migrations.AddField(
            model_name='statset',
            name='cs_at_10',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='statset',
            name='cs_at_20',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='statset',
            name='cs_at_30',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='statset',
            name='csd_at_10',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='statset',
            name='csd_at_20',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='statset',
            name='csd_at_30',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='statset',
            name='dmg_taken_at_10',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='statset',
            name='dmg_taken_at_20',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='statset',
            name='dmg_taken_at_30',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='statset',
            name='dmg_taken_diff_at_10',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='statset',
            name='dmg_taken_diff_at_20',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='statset',
            name='dmg_taken_diff_at_30',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='statset',
            name='gold_at_10',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='statset',
            name='gold_at_20',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='statset',
            name='gold_at_30',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='statset',
            name='pink_wards_killed_at_10',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='statset',
            name='pink_wards_killed_at_20',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='statset',
            name='pink_wards_killed_at_30',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='statset',
            name='pink_wards_placed_at_10',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='statset',
            name='pink_wards_placed_at_20',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='statset',
            name='pink_wards_placed_at_30',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='statset',
            name='trinket_wards_killed_at_10',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='statset',
            name='trinket_wards_killed_at_20',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='statset',
            name='trinket_wards_killed_at_30',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='statset',
            name='trinket_wards_placed_at_10',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='statset',
            name='trinket_wards_placed_at_20',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='statset',
            name='trinket_wards_placed_at_30',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='statset',
            name='xp_at_10',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='statset',
            name='xp_at_20',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='statset',
            name='xp_at_30',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='statset',
            name='yellow_wards_killed_at_10',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='statset',
            name='yellow_wards_killed_at_20',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='statset',
            name='yellow_wards_killed_at_30',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='statset',
            name='yellow_wards_placed_at_10',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='statset',
            name='yellow_wards_placed_at_20',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='statset',
            name='yellow_wards_placed_at_30',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
