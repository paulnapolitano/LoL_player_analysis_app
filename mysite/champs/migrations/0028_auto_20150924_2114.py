# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('champs', '0027_auto_20150924_2055'),
    ]

    operations = [
        migrations.RenameField(
            model_name='statset',
            old_name='firstBlood_assist',
            new_name='first_blood_assist',
        ),
        migrations.RenameField(
            model_name='statset',
            old_name='firstBlood_kill',
            new_name='first_blood_kill',
        ),
        migrations.RenameField(
            model_name='statset',
            old_name='firstInhibitor_assist',
            new_name='first_inhibitor_assist',
        ),
        migrations.RenameField(
            model_name='statset',
            old_name='firstInhibitor_kill',
            new_name='first_inhibitor_kill',
        ),
    ]
