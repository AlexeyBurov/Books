# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-27 17:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_site', '0015_materialdealerprice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dealer',
            name='dealer_amount',
            field=models.FloatField(default=0.0),
        ),
    ]
