# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-04 19:06
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_site', '0038_remove_order_dealer_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateField(default=datetime.datetime.now),
        ),
    ]
