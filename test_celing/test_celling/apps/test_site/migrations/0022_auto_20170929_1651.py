# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-29 13:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_site', '0021_celling_material_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='celling',
            name='for_remove',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='dealer',
            name='for_remove',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='for_remove',
            field=models.BooleanField(default=False),
        ),
    ]
