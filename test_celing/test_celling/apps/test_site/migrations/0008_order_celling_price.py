# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-22 13:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_site', '0007_remove_dialer_dialer_discount_percent'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='celling_price',
            field=models.FloatField(null=True),
        ),
    ]
