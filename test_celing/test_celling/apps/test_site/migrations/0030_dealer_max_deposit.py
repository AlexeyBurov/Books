# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-01 23:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_site', '0029_auto_20171002_0227'),
    ]

    operations = [
        migrations.AddField(
            model_name='dealer',
            name='max_deposit',
            field=models.FloatField(default=500.0),
        ),
    ]
