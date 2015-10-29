# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('champs', '0050_auto_20151026_2041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statset',
            name='assists',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='statset',
            name='champ_level',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='statset',
            name='deaths',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='statset',
            name='double_kills',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='statset',
            name='gold_earned',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='statset',
            name='gold_spent',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='statset',
            name='inhibitor_kills',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='statset',
            name='item_0',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='statset',
            name='item_1',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='statset',
            name='item_2',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='statset',
            name='item_3',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='statset',
            name='item_4',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='statset',
            name='item_5',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='statset',
            name='item_6',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='statset',
            name='killing_sprees',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='statset',
            name='kills',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='statset',
            name='largest_critical_strike',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='statset',
            name='largest_killing_spree',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='statset',
            name='largest_multi_kill',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='statset',
            name='magic_damage_dealt',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='statset',
            name='magic_damage_dealt_to_champions',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='statset',
            name='magic_damage_taken',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='statset',
            name='minions_killed',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='statset',
            name='neutral_minions_killed',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='statset',
            name='neutral_minions_killed_enemy_jungle',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='statset',
            name='neutral_minions_killed_team_jungle',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='statset',
            name='penta_kills',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='statset',
            name='physical_damage_dealt',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='statset',
            name='physical_damage_dealt_to_champions',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='statset',
            name='physical_damage_taken',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='statset',
            name='quadra_kills',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='statset',
            name='sight_wards_bought_in_game',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='statset',
            name='total_damage_dealt',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='statset',
            name='total_damage_dealt_to_champions',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='statset',
            name='total_damage_taken',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='statset',
            name='total_heal',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='statset',
            name='total_time_crowd_control_dealt',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='statset',
            name='total_units_healed',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='statset',
            name='tower_kills',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='statset',
            name='triple_kills',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='statset',
            name='true_damage_dealt',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='statset',
            name='true_damage_dealt_to_champions',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='statset',
            name='true_damage_taken',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='statset',
            name='unreal_kills',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='statset',
            name='vision_wards_bought_in_game',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='statset',
            name='wards_killed',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='statset',
            name='wards_placed',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
